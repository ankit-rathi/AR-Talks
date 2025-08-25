import json
import base64
import time
from confluent_kafka import Producer, KafkaException, KafkaError


def delivery_report(err, msg):
    """Delivery callback for Producer.produce"""
    if err is not None:
        logger.error("Failed to deliver message: %s", err)
    else:
        logger.info(
            "Message delivered to %s [%d] @ offset %d",
            msg.topic(), msg.partition(), msg.offset()
        )


def test_write_kafka(kafka_creds_dict, kafka_producer_config_dict, kafka_source_msg_dict):
    try:
        # === 1. Fetch secrets ===
        secrets = get_secrets_from_secret_manager(
            kafka_creds_dict['secret_name'],
            kafka_creds_dict['region']
        )

        # === 2. Write SSL certs to files ===
        ssl_cafile_path = "/var/tmp/kafka_ssl_cafile.pem"
        ssl_certfile_path = "/var/tmp/kafka_ssl_certfile.pem"
        ssl_keyfile_path = "/var/tmp/kafka_ssl_keyfile.key"

        with open(ssl_cafile_path, "w", encoding='utf-8') as ca_file:
            ca_file.write(base64.b64decode(secrets[kafka_creds_dict["secrets_ssl_cafile"]]).decode('utf-8'))
        with open(ssl_certfile_path, "w", encoding='utf-8') as cert_file:
            cert_file.write(base64.b64decode(secrets[kafka_creds_dict["secrets_ssl_certfile"]]).decode('utf-8'))
        with open(ssl_keyfile_path, "w", encoding='utf-8') as key_file:
            key_file.write(base64.b64decode(secrets[kafka_creds_dict["secrets_ssl_keyfile"]]).decode('utf-8'))

        # === 3. Confluent Producer Config ===
        producer_conf = {
            "bootstrap.servers": secrets[kafka_creds_dict['secrets_kafka_wt_brokers']],
            "security.protocol": kafka_producer_config_dict['security_protocol'],
            "ssl.ca.location": ssl_cafile_path,
            "ssl.certificate.location": ssl_certfile_path,
            "ssl.key.location": ssl_keyfile_path,
            "ssl.key.password": secrets[kafka_creds_dict['secrets_ssl_pwd']],
        }

        producer = Producer(producer_conf)

        # === 4. Serialize message ===
        message = json.dumps(kafka_source_msg_dict)

        # === 5. Produce message ===
        try:
            producer.produce(
                topic=kafka_producer_config_dict['topic_name'],
                value=message.encode("utf-8"),
                callback=delivery_report
            )

            # Poll to ensure delivery callback is triggered
            producer.flush(timeout=10)
            logger.info("Message successfully written to Kafka")
            return True

        except BufferError as buf_err:
            logger.error("Local producer queue is full: %s", buf_err)
            raise buf_err

        except KafkaException as kafka_write_error:
            logger.error("Failed to send message to Kafka: %s", kafka_write_error)
            raise kafka_write_error

    except KafkaError as kafka_err:
        logger.error("Kafka error: %s", kafka_err)
        raise kafka_err

    except Exception as e:
        logger.error("Unexpected error while writing to Kafka: %s", e)
        raise e
