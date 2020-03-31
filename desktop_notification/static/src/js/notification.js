/* © 2016 ClearCorp
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
 */
openerp.desktop_notification = function(session){
    "use strict"
    openerp.desktop_notification.Notification = openerp.Widget.extend({
        init: function(){
            this._super();
            var self = this;
            var def = window.Notification.requestPermission();
            this.sessions = {};
            this.bus = openerp.bus.bus;
            this.bus.on("notification", this, this.on_notification);
            this.set("session", openerp.session);
            this.desktop_session = new openerp.web.Model("desktop.session");
            var self = this;
            var user_id = 19;
            self.desktop_session.call('session_get', [user_id]).then(function(session_id){
                session_id = JSON.parse(session_id);
                self.bus.add_channel(session_id.uuid);
            });
        },
        on_notification: function(notification){
            var self = this;
            var channel = notification[0];
            var message = notification[1];
            var regex_uuid = new RegExp(/(\w{8}(-\w{4}){3}-\w{12}?)/g);
            
            if (regex_uuid.test(channel)) {
                if (message.type === "notification") {
                    this.send_native_notification(message.model, message.record_name);
                }
            }
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
    });    
    var notif = new openerp.desktop_notification.Notification();
}
