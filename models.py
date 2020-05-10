from flaskapp import db


class PushMap(db.Model):
    __tablename__ = 'haowu_push_map'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    push_token = db.Column(db.String(128), index=True)
    openid = db.Column(db.String(128))

    @staticmethod
    def insert_or_update(push_map):
        m = PushMap.query.filter(PushMap.push_token == push_map["push_token"]).first()
        if not m:
            m = PushMap(**push_map)
            db.session.add(m)
        else:
            m.openid = push_map["openid"]
        db.session.commit()


if __name__ == '__main__':
    PushMap.insert_or_update({
        "push_token": "123456",
        "openid": "kjhkj"
    })