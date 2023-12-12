class FixedSizeQueue {
    constructor(size = 10) {
        this.size = size;
        this.queue = [];
    }

    enqueue(element) {
        if (this.queue.length === this.size) {
            // Remove the oldest element (last in the array)
            this.queue.shift();
        }
        // Add the new element to the front of the array
        this.queue.push(element);
        // console.log("Queue size:", this.queue.length);
    }

    dequeue() {
        // Remove and return the oldest element (last in the array)
        return this.queue.shift();
    }

    clear() {
        this.queue = []
    }

    peek() {
        // Look at the next element to be dequeued without removing it
        return this.queue[0];
    }

    isEmpty() {
        // Check if the queue is empty
        return this.queue.length === 0;
    }

    isFull() {
        // Check if the queue is full
        return this.queue.length === this.size;
    }
}

// Example usage
// let queue = new FixedSizeQueue();

// for (let i = 1; i <= 12; i++) {
//     queue.enqueue(i);
//     console.log(queue.queue); // Display the current state of the queue
// }
