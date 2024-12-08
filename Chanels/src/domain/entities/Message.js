class Message {
    constructor(subject, username, content, contact) {
        this.subject = subject;
        this.username = username;
        this.content = content;
        this.contact = contact;
        this.timestamp = new Date();
    }
}

module.exports = Message;