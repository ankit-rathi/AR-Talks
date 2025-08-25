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
