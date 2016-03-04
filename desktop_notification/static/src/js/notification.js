/* © <YEAR(S)> ClearCorp
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
 */
openerp.desktop_notification = function(session){
    "use strict"
    //var def = window.Notification.requestPermission();
    
    openerp.desktop_notification.Notification = Backbone.Model.extend({
        initialize: function(session){
            var self = this;
           
            Backbone.Model.prototype.initialize.call(session);
            var odoo = new openerp.web.CompoundContext();
            console.log("odoo: ", odoo);
            this.session = session;
            console.log("backbone: ", this);
            console.log("session: ", session);
            var desktop_session = new openerp.web.Model("desktop.session");
            var user_id = 5;
            console.log("user id: ", user_id);
            desktop_session.call('session_get', [user_id]).then(function(session_id){
                    console.log("session_id: ", session_id);
                });
            
            console.log(desktop_session);
            
            this.sessions = {};
            this.bus = openerp.bus.bus;
            this.bus.on("desktop_notification", this, this.on_notification);
            
        },
        on_notification: function(notification){
             console.log("desktop_notification: ", notification);
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
    var notif = new openerp.desktop_notification.Notification(session);
}