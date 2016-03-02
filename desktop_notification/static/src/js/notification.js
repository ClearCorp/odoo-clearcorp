/* © <YEAR(S)> ClearCorp
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
 */
openerp.desktop_notification = function(session){
    var def = window.Notification.requestPermission();
    
    console.log(session);
    var _t = openerp._t;
    var _lt = openerp._lt;
    var QWeb = openerp.qweb;
    var NBR_LIMIT_HISTORY = 20;
    var USERS_LIMIT = 20;
    init = function(parent, options){
        this.sessions = {};
        this.bus = openerp.bus.bus;
        this.bus.on("notification", this, this.on_notification);
    }
    openerp.desktop_notification = function(session){
        
    }
    
    
    session.im_chat.ConversationManager.include({
        init: function(parent, options){
            this._super()
            this.bus.on('notification', this, this.on_notification2);
        },
        send_native_notification: function(title, content) {
            var notification = new Notification(title, {body: content, icon: 'web/binary/company_logo'});
            notification.onclick = function (e) {
                window.focus();
                if (this.cancel) {
                    this.cancel();
                } else if (this.close) {
                    this.close();
                }
            };
        },
        on_notification2: function(notification){
            this.send_native_notification("segunda funcion de notificacion", "Mensaje");
        },
        on_notification: function(notification) {   
            var self = this;
            var channel = notification[0];
            var message = notification[1];
            var regex_uuid = new RegExp(/(\w{8}(-\w{4}){3}-\w{12}?)/g);
            console.log('Nuevo javascript')

            // Concern im_chat : if the channel is the im_chat.session or im_chat.status, or a 'private' channel (aka the UUID of a session)
            if((Array.isArray(channel) && (channel[1] === 'im_chat.session' || channel[1] === 'im_chat.presence')) || (regex_uuid.test(channel))){
                
                // message to display in the chatview
                if (message.type === "message" || message.type === "meta") {
                    self.received_message(message);
                    this.send_native_notification('From: ' + message.from_id[1], message.message);
                    //console.log(channel);
                    //console.log(message);
                }
                // activate the received session
                if(message.uuid){
                    this.apply_session(message);
                }
                // user status notification
                if(message.im_status){
                    self.trigger("im_new_user_status", [message]);
                }
            }
        },
    });
}