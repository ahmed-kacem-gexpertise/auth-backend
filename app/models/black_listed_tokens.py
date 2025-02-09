from datetime import datetime
from ..extensions import db 
class BlacklistedToken(db.Model):
    __tablename__ = "blacklisted_tokens"

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(255), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, jti):
        self.jti = jti

    def save(self):
        db.session.add(self)
        db.session.commit()
