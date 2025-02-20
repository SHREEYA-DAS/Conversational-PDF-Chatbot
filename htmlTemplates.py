css = '''
<style>
.chat-message {
    padding: 1.5rem; 
    border-radius: 1rem; /* Increased border-radius for more rounded corners */
    margin-bottom: 1rem; 
    display: flex;
}
.chat-message.user {
    background-color: #2b313e;
    border-radius: 10px; /* Increased border-radius for more rounded corners */
}
.chat-message.bot {
    background-color: #475063;
    border-radius: 10px; /* Increased border-radius for more rounded corners */
}
.chat-message .avatar {
    width: 60px; height: 60px; border-radius: 50%; object-fit: cover;
    padding: 10px;
}
.chat-message .avatar img {
    width: 60px; height: 60px; border-radius: 50%; object-fit: cover;
    padding: 10px;
}
.chat-message .message {
    width: 80%;
    padding: 1.5rem;
    color: #fff;
}
</style>
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://cdn-icons-png.flaticon.com/512/11306/11306137.png" style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://cdn-icons-png.flaticon.com/512/9187/9187604.png" style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''
