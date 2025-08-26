import json
import base64
import time
from datetime import datetime
import signal
from confluent_kafka import Consumer, KafkaException, KafkaError


def test_read_kafka(kafka_creds_dict, kafka_topic_config_dict, kafka_consumer_config_dict, execution_details_dict, kwargs):
    retry = kafka_consumer_config_dict.get('retries', 5)

    while retry > 0:
        try:
            # === 1. Fetch secrets from secret manager ===
            secrets = get_secrets_from_secret_manager(
                kafka_creds_dict['secret_name'],
                kafka_creds_dict['region']
            )

            ssl_cafile_path = "/var/tmp/kafka_ssl_cafile.pem"
            ssl_certfile_path = "/var/tmp/kafka_ssl_certfile.pem"
            ssl_keyfile_path = "/var/tmp/kafka_ssl_keyfile.key"

            # Write SSL files
            with open(ssl_cafile_path, "w", encoding='utf-8') as ca_file:
                ca_file.write(base64.b64decode(secrets[kafka_creds_dict["secrets_ssl_cafile"]]).decode('utf-8'))
            with open(ssl_certfile_path, "w", encoding='utf-8') as cert_file:
                cert_file.write(base64.b64decode(secrets[kafka_creds_dict["secrets_ssl_certfile"]]).decode('utf-8'))
            with open(ssl_keyfile_path, "w", encoding='utf-8') as key_file:
                key_file.write(base64.b64decode(secrets[kafka_creds_dict["secrets_ssl_keyfile"]]).decode('utf-8'))

            # === 2. Confluent Kafka Consumer Config ===
            consumer_conf = {
                "bootstrap.servers": secrets[kafka_creds_dict['secrets_kafka_wt_brokers']],
                "group.id": kafka_topic_config_dict['consumer_group'],
                "auto.offset.reset": kafka_consumer_config_dict['auto_offset_reset'],
                "enable.auto.commit": kafka_consumer_config_dict['enable_auto_commit'],
                "security.protocol": kafka_consumer_config_dict['security_protocol'],
                "ssl.ca.location": ssl_cafile_path,
                "ssl.certificate.location": ssl_certfile_path,
                "ssl.key.location": ssl_keyfile_path,
                "ssl.key.password": secrets[kafka_creds_dict['secrets_ssl_pwd']],
                "max.poll.interval.ms": kafka_consumer_config_dict['max_poll_interval_ms'],
                "request.timeout.ms": kafka_consumer_config_dict['request_timeout_ms'],
                "connections.max.idle.ms": kafka_consumer_config_dict['connections_max_idle_ms'],
                # consumer_timeout_ms in kafka-python is not direct; emulate via poll timeout
            }

            consumer = Consumer(consumer_conf)
            consumer.subscribe([kafka_topic_config_dict['topic_name']])

            # === 3. Poll messages ===
            while True:
                msg = consumer.poll(timeout=1.0)  # poll with 1 second timeout
                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        # End of partition event, safe to ignore
                        continue
                    raise KafkaException(msg.error())

                # === 4. Decode message ===
                message_data = json.loads(msg.value().decode('utf-8'))

                # === 5. Check condition ===
                if safe_evaluate_condition(execution_details_dict['pt_message_check_condition'], message_data):
                    xcom_key = datetime.now().strftime("%Y%m%d%H%M%S")
                    message_to_emr_dict = {
                        "request_uid": header['request_uid'],
                        "airflow_status": 'PASS',
                        "source": "read_kafka_message",
                        "message": message_data
                    }
                    kwargs['ti'].xcom_push(key=xcom_key, value=message_to_emr_dict)

                    # Manual commit example if needed
                    # consumer.commit(asynchronous=True)

                    return xcom_key

        except (KafkaException, KafkaError, FileNotFoundError, ValueError) as kafka_connection_exception:
            retry -= 1
            if retry > 0:
                logger.info("Retrying in %s seconds…", kafka_consumer_config_dict.get('retry_delay', 60))
                time.sleep(kafka_consumer_config_dict.get('retry_delay', 60))
                continue
            logger.error("Kafka connection exception due to %s", kafka_connection_exception)
            raise kafka_connection_exception
        finally:
            try:
                consumer.close()
            except Exception:
                pass


from confluent_kafka import Consumer, KafkaException, KafkaError
import logging
import json

def kafka_listener(config_dict, **kwargs):
    kafka_creds_dict = config_dict['kafka']['kafka_credential_details']
    kafka_consumer_config_dict = config_dict['kafka']['kafka_consumer_config']
    kafka_topic_config_dict = config_dict['kafka']['external_topic']

    # Build Consumer configuration (Confluent style)
    consumer_conf = {
        'bootstrap.servers': kafka_creds_dict['bootstrap_servers'],
        'security.protocol': kafka_consumer_config_dict['security_protocol'],
        'ssl.ca.location': kafka_consumer_config_dict.get('ssl_cafile'),
        'ssl.certificate.location': kafka_consumer_config_dict.get('ssl_certfile'),
        'ssl.key.location': kafka_consumer_config_dict.get('ssl_keyfile'),
        'ssl.key.password': kafka_consumer_config_dict.get('ssl_password'),
        'group.id': kafka_consumer_config_dict['group_id'],
        'auto.offset.reset': kafka_consumer_config_dict.get('auto_offset_reset', 'earliest'),
        'enable.auto.commit': False  # Manual commit like kafka-python
    }

    consumer = Consumer(consumer_conf)
    topic_name = kafka_topic_config_dict['topic_name']
    consumer.subscribe([topic_name])

    expected_message_count = 0
    offset_to_read_from = None

    try:
        while True:
            msg = consumer.poll(timeout=5.0)  # Poll messages
            if msg is None:
                logging.info("No messages received in this poll cycle.")
                break
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    logging.info(f"End of partition reached {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")
                    continue
                else:
                    raise KafkaException(msg.error())

            try:
                key = msg.key().decode('utf-8') if msg.key() else None
                value = msg.value().decode('utf-8')
                logging.info("Message offset=%s, partition=%s, key=%s, value=%s",
                             msg.offset(), msg.partition(), key, value)
                offset_to_read_from = f"{msg.offset()},{msg.partition()}"

                consumer.commit(msg)  # Manual commit
                expected_message_count += 1
                break  # exit loop after one message (as per your logic)

            except json.JSONDecodeError:
                logging.error("Can't decode Kafka message")
                logging.error("Skipping processing of message at offset %d", msg.offset())
            except Exception as exc:
                logging.error("Caught error while processing Kafka message", exc_info=True)
                raise exc

    except KafkaException as exc:
        logging.error("Kafka error occurred", exc_info=True)
        raise exc
    finally:
        consumer.close()

    if expected_message_count > 0:
        kwargs['ti'].xcom_push(key='message_offset', value=offset_to_read_from)
        return "emr_connection_creator"

    return "skipped"


from confluent_kafka import Consumer, KafkaError, KafkaException
import boto3
import json
import logging

def confluent_kafka_listener(config_dict, config):
    try:
        # Initialize S3 client
        s3_client = boto3.client('s3')

        # Extract Kafka configs
        kafka_creds_dict = config_dict['kafka']['kafka_credential_details']
        kafka_consumer_config_dict = config_dict['kafka']['kafka_consumer_config']
        kafka_topic_config_dict = config_dict['kafka']['internal_topic']

        # Build Consumer configuration
        consumer_conf = {
            'bootstrap.servers': kafka_creds_dict['bootstrap_servers'],
            'security.protocol': kafka_consumer_config_dict.get('security_protocol', 'SSL'),
            'ssl.ca.location': kafka_creds_dict.get('ssl_ca_location'),
            'ssl.certificate.location': kafka_creds_dict.get('ssl_cert_location'),
            'ssl.key.location': kafka_creds_dict.get('ssl_key_location'),
            'ssl.key.password': kafka_creds_dict.get('ssl_password'),
            'group.id': kafka_consumer_config_dict.get('group_id', 'default_group'),
            'auto.offset.reset': kafka_consumer_config_dict.get('auto_offset_reset', 'earliest'),
            'enable.auto.commit': False
        }

        consumer = Consumer(consumer_conf)
        consumer.subscribe([kafka_topic_config_dict['topic_name']])
        logging.info("Subscribed to Kafka topic: %s", kafka_topic_config_dict['topic_name'])

        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue  # No message this poll cycle
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    logging.info("End of partition reached %s [%d] at offset %d",
                                 msg.topic(), msg.partition(), msg.offset())
                    continue
                else:
                    raise KafkaException(msg.error())

            # Process message
            logging.info("Message offset: %s, partition: %s, key: %s, value: %s",
                         msg.offset(), msg.partition(), msg.key(), msg.value())

            message_value = json.loads(msg.value().decode('utf-8'))
            json_data = json.dumps(message_value)
            logging.info('Printing message_value: %s', message_value)

            message_value_validation_list = config['dynamic_dag_pattern_file']['message_value_validation_list']
            if all(value in message_value for value in message_value_validation_list):
                message_value_validation_list_values = {
                    key: message_value[key] for key in message_value_validation_list if key in message_value
                }

                # File name construction
                file_name = (config['dag_naming_convention']['dag_name_prefix'] + "_" +
                             config['dag_naming_convention']['dag_name_suffix']).format(
                             **message_value_validation_list_values)
                file_name = ''.join(c for c in file_name if c.isalnum() or c == '_') + '.json'

                # Upload to S3
                s3_client.put_object(
                    Bucket=config_dict['airflow']['s3_bucket'],
                    Key=f"{config_dict['airflow']['script_path']}/"
                        f"{config_dict['dynamic_dag_pattern_file']['file_path']}/{file_name}",
                    Body=json_data
                )
                logging.info("Uploaded file %s to S3", file_name)

                # Commit this message offset
                consumer.commit(msg)

    except KafkaException as ke:
        logging.error("Kafka error occurred", exc_info=True)
        raise ke
    except Exception as e:
        logging.error("Unexpected error occurred", exc_info=True)
        raise e
    finally:
        consumer.close()
        logging.info("Kafka consumer closed.")


