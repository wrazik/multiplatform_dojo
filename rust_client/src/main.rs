use std::thread;
use std::time::Duration;

fn main() {
    let context = zmq::Context::new();
    let subscriber = context.socket(zmq::SUB).unwrap();
    subscriber
        .connect("tcp://localhost:8080")
        .expect("failed connecting subscriber");
    subscriber
        .set_subscribe(b"42")
        .expect("failed setting subscription");
    thread::sleep(Duration::from_millis(1));

    loop {
        let message = subscriber
            .recv_string(0)
            .expect("failed receiving update")
            .unwrap();
        println!("[RECV] {}", message);
    }
}
