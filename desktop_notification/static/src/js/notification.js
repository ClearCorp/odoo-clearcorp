/* © <YEAR(S)> ClearCorp
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
 */
openerp.desktop_notification = function(session){
    "use strict"
    //var def = window.Notification.requestPermission();
    
    openerp.desktop_notification.Notification = openerp.Widget.extend({
        init: function(){
            this._super();
            var self = this;
            this.sessions = {};
            this.bus = openerp.bus.bus;
            this.bus.on("notification", this, this.on_notification);
            this.set("session", openerp.session);
            this.desktop_session = new openerp.web.Model("desktop.session");
            console.log("init wifget");
            var self = this;
            console.log("bus: ", self.bus);
            console.log("session: ", this.get("session"));
            var user_id = 19;
            console.log("user id: ", user_id);
            self.desktop_session.call('session_get', [user_id]).then(function(session_id){
                
                console.log("bus: ", self.bus);
                session_id = JSON.parse(session_id);
                console.log("session_id: ", session_id);
                self.bus.add_channel(session_id.uuid);
                self.bus.add_channel('[cc_notificaciones, desktop.session, 21]')
                self.bus.add_channel("123456789")
                
                console.log("uuid: ", session_id.uuid);
                console.log("channels: ", self.bus.channels);
            });
            
            
        },
        start: function(){
            
            //console.log(this.desktop_session["uuid"]);
            
        },
        on_notification: function(notification){
            console.log("desktop_notification: ", notification);
            var self = this;
            var channel = notification[0];
            var message = notification[1];
            var regex_uuid = new RegExp(/(\w{8}(-\w{4}){3}-\w{12}?)/g);

            if((Array.isArray(channel) && (channel[1] === 'desktop.session'))){
                console.log("desktop session confirmed");
            }
        }
    });
    
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
            console.log('Nuevo javascript', notification);

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
    
    var notif = new openerp.desktop_notification.Notification();
}
