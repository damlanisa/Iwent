import psycopg2 as dbapi2
from flask import current_app as app
from flask_login import UserMixin
from Iwent import login_manager
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    users = User().retrieve('*', f"id = {user_id}")
    if users:
        user = users[0]
    else:
        user = None
    return user


class BaseModel:
    def __init__(self, url=None):
        self.connection_url = app.config["DATABASE_URI"]

    def create(self):
        pass

    def update(self):
        pass

    def retrieve(self):
        pass

    def delete(self):
        pass

    def execute(self, statement, variables=None, fetch=False):
        response = None
        with dbapi2.connect(self.connection_url) as connection:
            with connection.cursor() as cursor:
                cursor.execute(statement, variables)
                if fetch:
                    response = cursor.fetchall()
        return response

    def join(self, queryKey, condition=None, variables=None):
        pass


class User(BaseModel, UserMixin):
    def __init__(self, user_id=None, username=None, firstname=None,
                 lastname=None, email=None, password=None):
        super(User, self).__init__()
        self.user_id = user_id
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password
        self.date_created = datetime.today()
        self.date_updated = datetime.today()
        print(datetime.today())

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

    def create(self):
        statement = """
        insert into users (username, firstname, lastname,
        email, password, date_created, date_updated)
        values (%s, %s, %s, %s, %s, %s, %s)
        """

        self.execute(statement, (self.username, self.firstname, self.lastname, self.email, self.password,
                     self.date_created, self.date_updated))

    def update(self):
        statement = """
        update users set username = %s, firstname = %s,
        lastname = %s, date_updated = %s where id = %s
        """
        self.execute(statement, (self.username, self.firstname,
                                 self.lastname, self.date_updated, self.user_id))

    def retrieve(self, queryKey, condition=None, variables=None):
        statement = f"""
        select {queryKey} from users"""
        if (condition):
            statement += f"""
            where {condition}
            """
        userDatas = self.execute(statement, variables, fetch=True)
        if queryKey == '*':
            users = []
            for userData in userDatas:
                user = User(user_id=userData[0],
                            username=userData[3],
                            firstname=userData[4],
                            lastname=userData[5],
                            email=userData[6],
                            password=userData[7])
                users.append(user)
            return users
        return userDatas

    def delete(self, condition=None, variables=None):
        statement = f"""
        delete from users
        """
        if (condition):
            statement += f"""
            where {condition}
            """
        self.execute(statement, variables, fetch=False)

    def get_id(self):
        return str(self.user_id)


class Event(BaseModel):
    def __init__(self, creator=None, event_id=None, event_name=None, event_type=None,
                 is_private=None, event_date=None):
        super(Event, self).__init__()
        self.creator = creator
        self.event_id = event_id
        self.event_name = event_name
        self.event_type = event_type
        self.is_private = is_private
        self.event_date = event_date

    def __repr__(self):
        return f"User('{self.event_name}', '{self.event_type}')"

    def create(self):
        statement = """
        insert into events (creator, name, type, is_private, date)
        values (%s, %s, %s, %s, %s)
        """
        self.execute(statement, (self.creator, self.event_name, self.event_type,
                                 self.is_private, self.event_date))

    def update(self):
        statement = """
        update events set name = %s,  type = %s, date = %s
        """
        self.execute(statement, (self.event_name, self.event_type, self.event_date))

    def retrieve(self, queryKey, condition=None, variables=None):
        statement = f"""
        select {queryKey} from events"""
        if (condition):
            statement += f"""
            where {condition}
            """
        eventDatas = self.execute(statement, variables, fetch=True)
        if queryKey == '*':
            events = []
            for eventData in eventDatas:
                event = Event(event_id=eventData[0],
                              event_name=eventData[1],
                              event_type=eventData[4],
                              creator=eventData[5],
                              event_date=eventData[7])
                events.append(event)
            return events
        return eventDatas

    def delete(self, condition=None, variables=None):
        statement = f"""
        delete from events
        """
        if (condition):
            statement += f"""
            where {condition}
            """
        self.execute(statement, variables, fetch=False)


class Address(BaseModel):
    def __init__(self, address_id=None, address_name=None, address_country=None,
                 address_city=None, address_line1=None, address_line2=None):
        super(Address, self).__init__
        self.address_id = address_id
        self.address_name = address_name
        self.address_country = address_country
        self.address_city = address_city
        self.address_line1 = address_line1
        self.address_line2 = address_line2

    def create(self):
        statement = """
        insert into addresses (name, country, city, line1, line2)
        values (%s, %s, %s, %s, %s)
        """
        self.execute(statement, (self.address_name, self.address_country, self.address_city,
                     self.address_line1, self.address_line2))

    def retrieve(self, queryKey, condition=None, variables=None):
        statement = f"""
        select {queryKey} from addresses"""
        if(condition):
            statement += f"""
            where {condition}
            """
        addressDatas = self.execute(statement, variables, fetch=True)
        if queryKey == '*':
            addresses = []
            for addressData in addressDatas:
                address = Address(address_id=addressData[0],
                                  address_name=addressData[1],
                                  address_country=addressData[2],
                                  address_city=addressData[3],
                                  address_line1=addressData[4],
                                  address_line2=addressData[5])
                addresses.append(address)
            return addresses
        return addressDatas


class EventType(BaseModel):
    def __init__(self, eventtype_id=None, eventtype_name=None, eventtype_information=None,
                 eventtype_counter=None):
        super(EventType, self).__init__
        self.eventtype_id = eventtype_id
        self.eventtype_name = eventtype_name
        self.eventtype_information = eventtype_information
        self.eventtype_counter = eventtype_counter

    def create(self):
        statement = """
        insert into eventtypes (name, information, counter)
        values (%s, %s, %s)
        """
        self.execute(statement, (self.eventtype_name, self.eventtype_information, self.eventtype_counter))

    def retrieve(self, queryKey, condition=None, variables=None):
        statement = f"""
        select {queryKey} from eventtypes"""
        if(condition):
            statement += f"""
            where {condition}
            """
        eventTypeDatas = self.execute(statement, variables, fetch=True)
        if queryKey == '*':
            eventTypes = []
            for eventTypeData in eventTypeDatas:
                eventType = eventTypes(eventtype_id=eventTypeData[0],
                                  eventtype_name=eventTypeData[1],
                                  eventtype_information=eventTypeData[2],
                                  eventtype_counter=eventTypeData[3],)
                eventTypes.append(eventType)
            return eventTypes
        return eventTypeDatas
