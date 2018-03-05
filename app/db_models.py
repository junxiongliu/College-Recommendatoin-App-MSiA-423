from app import db

# Create a data model for the database to be setup for the app
class college(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    INSTNM = db.Column(db.String(100), unique=False, nullable=False)
    CITY = db.Column(db.String(100), unique=False, nullable=True)
    state = db.Column(db.String(100), unique=False, nullable=True)
    degree_offered = db.Column(db.Integer, unique=False, nullable=True)
    CONTROL = db.Column(db.Integer, unique=False, nullable=True)
    region = db.Column(db.Integer, unique=False, nullable=True)
    ADM_RATE = db.Column(db.Float, unique=False, nullable=True)
    SATVRMID = db.Column(db.Integer, unique=False, nullable=True)
    SATMTMID = db.Column(db.Integer, unique=False, nullable=True)
    num_undergrad = db.Column(db.Integer, unique=False, nullable=True)
    prop_arts_human = db.Column(db.Float, unique=False, nullable=True)
    prop_business = db.Column(db.Float, unique=False, nullable=True)
    prop_health_med = db.Column(db.Float, unique=False, nullable=True)
    prop_interdiscip = db.Column(db.Float, unique=False, nullable=True)
    prop_public_svce = db.Column(db.Float, unique=False, nullable=True)
    prop_sci_math_tech = db.Column(db.Float, unique=False, nullable=True)
    prop_social_sci = db.Column(db.Float, unique=False, nullable=True)
    prop_trades_personal_svce = db.Column(db.Float, unique=False, nullable=True)
    
    def __repr__(self):
        return str([self.INSTNM, self.CITY, self.state, self.degree_offered, self.CONTROL, self.region, self.ADM_RATE, self.SATVRMID, self.SATMTMID, self.num_undergrad,
        self.prop_arts_human, self.prop_business, self.prop_health_med, self.prop_interdiscip, self.prop_public_svce, self.prop_sci_math_tech, self.prop_social_sci, self.prop_trades_personal_svce])