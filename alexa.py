from ask_sdk_core.dispatch_components import AbstractRequestHandler, AbstractExceptionHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from ask_sdk_model.ui import SimpleCard, LinkAccountCard
import requests
from flask_sqlalchemy import sqlalchemy, SQLAlchemy
# from run import perform_action
from _email import email
from flask import Flask, render_template, request, url_for, redirect, flash, session, abort
from iot import netcat

db_name = "auth.db"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{db}'.format(db=db_name)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# SECRET_KEY required for session, flash and Flask Sqlalchemy to work
app.config['SECRET_KEY'] = 'configure strong secret key here'

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'
    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    pass_hash = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return '' % self.username


class Device(db.Model):
    __tablename__ = 'device'
    did = db.Column(db.Integer, primary_key=True)
    dev_name = db.Column(db.String(100), unique=True, nullable=False)
    dev_ip = db.Column(db.String(100), nullable=False)
    username = db.Column(db.Integer, db.ForeignKey('user.username'))


def perform_action(email, dev_name, action):
    dev_name = dev_name.lower()
    action = action.upper()
    username = User.query.filter_by(email=email).first().username
    device = Device.query.filter_by(username=username,
                                    dev_name=dev_name).first()
    value = netcat(device.dev_ip, 4444, action)
    return value


URL = "https://api.amazon.com/user/profile?access_token="


def get_user_detail(access_token):
    return requests.get(URL + access_token).json()


class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        access_token = handler_input.request_envelope.context.system.user.access_token

        if (access_token == None):
            speech_text = "Please use Alexa companion app to authenticate"
            # speech_text = "Welcome to the Alexa Skills Kit, you can say hello!"

            handler_input.response_builder.speak(speech_text).set_card(
                LinkAccountCard()).set_should_end_session(False)
            return handler_input.response_builder.response

        else:
            speech_text = "This is the default message."
            data = get_user_detail(access_token)

            speech_text = f"Hi {data['name']}. I have your email address as: {data['email']}"

            handler_input.response_builder.speak(speech_text).set_card(
                SimpleCard("Got data",
                           speech_text)).set_should_end_session(False)
            return handler_input.response_builder.response


class HelloWorldIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("HelloWorldIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Hello World"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Hello World",
                       speech_text)).set_should_end_session(True)
        return handler_input.response_builder.response


class HelpIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "You can say hello to me!"

        handler_input.response_builder.speak(speech_text).ask(
            speech_text).set_card(SimpleCard("Hello World", speech_text))
        return handler_input.response_builder.response


class ToggleDeviceHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("ToggleDeviceIntent")(handler_input)

    def handle(self, handler_input):
        data = handler_input.request_envelope.request.intent.slots
        dev_name = "".join(data["device_name"].value.split())
        action = data["action"].value
        print(action)
        print(dev_name)
        response = perform_action(email, dev_name, action)
        handler_input.response_builder.speak("toggling device").set_card(
            SimpleCard("Toggle", "toggle")).set_should_end_session(False)
        return handler_input.response_builder.response


class GetDataIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("GetDataIntent")(handler_input)

    def handle(self, handler_input):

        speech_text = "pullu is love"
        data = handler_input.request_envelope.request.intent.slots
        dev_name = "".join(data["device_name"].value.split())

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Device Data",
                       speech_text)).set_should_end_session(False)
        return handler_input.response_builder.response


class CancelAndStopIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.CancelIntent")(
            handler_input) or is_intent_name("AMAZON.StopIntent")(
                handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Goodbye!"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Hello World",
                       speech_text)).set_should_end_session(True)
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        # any cleanup logic goes here

        return handler_input.response_builder.response


class AllExceptionHandler(AbstractExceptionHandler):
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        # Log the exception in CloudWatch Logs
        print(exception)

        speech = "Sorry, I didn't get it. Can you please say it again!!"
        handler_input.response_builder.speak(speech).ask(speech)
        return handler_input.response_builder.response