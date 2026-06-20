import time, smtplib, requests
from email.message import EmailMessage

class AlertManager:
    def __init__(self, cfg, db=None):
        self.cfg=cfg; self.db=db; self.last={}
    def _allowed(self, key):
        now=time.time(); cd=int(self.cfg.get('alert_cooldown_seconds',60))
        if now - self.last.get(key,0) >= cd:
            self.last[key]=now; return True
        return False
    def send(self, kind, message, image_path=None):
        if not self._allowed(kind): return {'sent':False,'reason':'cooldown'}
        if self.db: self.db.log(kind, 'danger' if kind in ['stranger','gas','fire'] else 'info', message)
        sent=[]
        if self.cfg.get('telegram_enabled') and self.cfg.get('telegram_bot_token') and self.cfg.get('telegram_chat_id'):
            try:
                url=f"https://api.telegram.org/bot{self.cfg['telegram_bot_token']}/sendMessage"
                requests.post(url, data={'chat_id':self.cfg['telegram_chat_id'],'text':message}, timeout=5)
                sent.append('telegram')
            except Exception as e:
                if self.db: self.db.log('alert_error','warning',str(e))
        if self.cfg.get('email_enabled') and self.cfg.get('smtp_username') and self.cfg.get('email_to'):
            try:
                msg=EmailMessage(); msg['Subject']='Sleep Safe Robot Alert'; msg['From']=self.cfg['smtp_username']; msg['To']=self.cfg['email_to']; msg.set_content(message)
                with smtplib.SMTP(self.cfg.get('smtp_host','smtp.gmail.com'), int(self.cfg.get('smtp_port',587))) as s:
                    s.starttls(); s.login(self.cfg['smtp_username'], self.cfg['smtp_password']); s.send_message(msg)
                sent.append('email')
            except Exception as e:
                if self.db: self.db.log('alert_error','warning',str(e))
        return {'sent':bool(sent),'channels':sent}
