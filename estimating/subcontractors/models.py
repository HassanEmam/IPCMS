'''


'''
from IPCMS import db


class Subcontractor(db.Model):
    __tablename__ = "subcontractors"
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(80), unique=True)
    name = db.Column(db.String(80))
    description = db.Column(db.Text)
    address = db.Column(db.Text)
    contact_number = db.Column(db.Text)
    contact_person = db.Column(db.Text)
    org_id = db.Column(db.Integer, db.ForeignKey('organisations.id'))
    organisation = db.relationship('Organisation', backref='subcontractors')
    status = db.Column(db.Boolean, default=True)

    __table_args__ = (
        db.UniqueConstraint('code', 'org_id', name='uix_subcon1'),
    )

    def __init__(self, code, name, description, address, contact_number, contact_person, organisation, status=True):
        self.code = code
        self.name = name
        self.description = description
        self.address = address
        self.contact_person = contact_person
        self.contact_number = contact_number
        self.org_id = organisation.id
        self.status = status

    def __repr__(self):
        return self.name


class SubcontractorCompanies(db.Model):
    __tablename__ = 'subcontractor_company'
    id = db.Column(db.Integer, primary_key=True)
    subcontractor_id = db.Column(db.Integer, db.ForeignKey('subcontractors.id'))
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    company = db.relationship("Company", backref="assoc_subcontractor")
    subcontractor = db.relationship("Subcontractor", backref="assoc")
    org_id = db.Column(db.Integer, db.ForeignKey('organisations.id'))
    organisation = db.relationship('Organisation', backref='subcontractorcompanies')
    is_active = db.Column(db.Boolean)

    __table_args__ = (
        db.UniqueConstraint('subcontractor_id', 'company_id', name='sc_cmp_1'),
    )

    def __init__(self, subcontractor, company, organisation, is_active=True):
        self.subcontractor_id = subcontractor.id
        self.company_id = company.id
        self.org_id = organisation.id
        self.is_active = is_active
