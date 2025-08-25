# kafka_config.yaml
kafka:
  bootstrap_servers: "localhost:9092"
  group_id: "demo-group"
  topics:
    - "demo-topic"
  auto_offset_reset: "earliest"      # "latest" or "earliest"
  enable_auto_commit: true           # or false
  # --- OPTIONAL AUTH (uncomment if needed) ---
  # security_protocol: "SASL_SSL"
  # sasl_mechanism: "PLAIN"          # for Confluent Cloud: "PLAIN"
  # sasl_plain_username: "<api_key>"
  # sasl_plain_password: "<api_secret>"
  # session_timeout_ms: 45000

###########BEFORE#################

# consumer_kafka_python.py
import json
import signal
import sys
import yaml
from kafka import KafkaConsumer

stop = False

def handle_sigint(signum, frame):
    global stop
    stop = True

signal.signal(signal.SIGINT, handle_sigint)
signal.signal(signal.SIGTERM, handle_sigint)

def main():
    with open("kafka_config.yaml") as f:
        cfg = yaml.safe_load(f)["kafka"]

    # kafka-python uses underscore-style keys and direct kwargs
    consumer = KafkaConsumer(
        *cfg.get("topics", []),
        bootstrap_servers=cfg["bootstrap_servers"],
        group_id=cfg.get("group_id"),
        auto_offset_reset=cfg.get("auto_offset_reset", "latest"),
        enable_auto_commit=cfg.get("enable_auto_commit", True),
        # Deserialization—you can replace with your own logic
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        # Optional security (kafka-python naming)
        security_protocol=cfg.get("security_protocol"),
        sasl_mechanism=cfg.get("sasl_mechanism"),
        sasl_plain_username=cfg.get("sasl_plain_username"),
        sasl_plain_password=cfg.get("sasl_plain_password"),
        session_timeout_ms=cfg.get("session_timeout_ms"),
    )

    try:
        while not stop:
            try:
                for msg in consumer:
                    if stop:
                        break
                    # msg.value is already deserialized by value_deserializer
                    process_message(msg.topic, msg.partition, msg.offset, msg.key, msg.value)
            except Exception as e:
                # Handle message loop errors (transient network, deserialization, etc.)
                handle_error(e)
    finally:
        consumer.close()

def process_message(topic, partition, offset, key, value):
    # Your domain logic here
    print(f"[kafka-python] {topic}:{partition}@{offset} key={key} value={value}")

def handle_error(e):
    # Your error logging/alerting
    print(f"[kafka-python] Error: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()


########AFTER##############

# consumer_confluent_kafka.py
import json
import signal
import sys
import yaml
from confluent_kafka import Consumer, KafkaError, KafkaException

stop = False

def handle_sigint(signum, frame):
    global stop
    stop = True

signal.signal(signal.SIGINT, handle_sigint)
signal.signal(signal.SIGTERM, handle_sigint)

def map_kafka_python_to_confluent(cfg):
    """
    Keep your YAML unchanged and map to confluent-kafka config keys.
    """
    m = {
        "bootstrap.servers": cfg["bootstrap_servers"],
        "group.id": cfg.get("group_id"),
        "auto.offset.reset": cfg.get("auto_offset_reset", "latest"),
        "enable.auto.commit": cfg.get("enable_auto_commit", True),
    }
    # Optional auth/security mapping
    if cfg.get("security_protocol"):
        m["security.protocol"] = cfg["security_protocol"]
    if cfg.get("sasl_mechanism"):
        # confluent uses plural "sasl.mechanisms"
        m["sasl.mechanisms"] = cfg["sasl_mechanism"]
    if cfg.get("sasl_plain_username"):
        m["sasl.username"] = cfg["sasl_plain_username"]
    if cfg.get("sasl_plain_password"):
        m["sasl.password"] = cfg["sasl_plain_password"]
    if cfg.get("session_timeout_ms"):
        m["session.timeout.ms"] = cfg["session_timeout_ms"]
    return {k: v for k, v in m.items() if v is not None}

def main():
    with open("kafka_config.yaml") as f:
        raw = yaml.safe_load(f)["kafka"]

    consumer_conf = map_kafka_python_to_confluent(raw)
    topics = raw.get("topics", [])

    consumer = Consumer(consumer_conf)

    # Subscribe instead of passing topics to constructor
    consumer.subscribe(topics)

    try:
        while not stop:
            try:
                msg = consumer.poll(1.0)   # seconds
                if msg is None:
                    continue

                if msg.error():
                    # Some errors are informational (e.g., partition EOF),
                    # but treat non-EOF as exceptions or log accordingly.
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        # End of partition event – often safe to ignore
                        continue
                    raise KafkaException(msg.error())

                # Manual deserialization (mirror your kafka-python value_deserializer)
                value = json.loads(msg.value().decode("utf-8")) if msg.value() is not None else None
                key = msg.key().decode("utf-8") if msg.key() else None

                process_message(msg.topic(), msg.partition(), msg.offset(), key, value)

                # If you disabled auto commit, you can commit manually:
                # consumer.commit(msg, asynchronous=True)

            except KafkaException as ke:
                handle_error(ke)
            except Exception as e:
                handle_error(e)
    finally:
        # Ensure a clean leave of the group and final commit if auto-commit is enabled
        consumer.close()

def process_message(topic, partition, offset, key, value):
    print(f"[confluent-kafka] {topic}:{partition}@{offset} key={key} value={value}")

def handle_error(e):
    print(f"[confluent-kafka] Error: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
