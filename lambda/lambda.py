"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
import boto3
import json

iot_client = boto3.client('iot-data')
AWS_IOT_PUBLISH_TOPIC = 'alexa-tv-remote'

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
      #  'card': {
      #      'type': 'Simple',
      #      'title': "SessionSpeechlet - " + title,
      #      'content': "SessionSpeechlet - " + output
      #  },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


def slot_has_value(intent, name):
    return (name in intent['slots']) and ('value' in intent['slots'][name])


def channel_to_numerical(channel_name_input):
    """ Converts the word representation of a channel into it's numerical value. """
    channel_name = channel_name_input.lower()
    mapping = {
                'itv': 3,
                'bbc two': 2,
                'e4 plus 1': 29,
                'e4': 28,
                'dave': 40,
                'challenge': 30,
                'bbc news': 130,
                'quest': 37,
                'quest plus 1': 38
               }

    if channel_name in mapping:
        return mapping[channel_name]
    else:
        print("failed to find word channel channel="+channel_name)
        return -1

# --------------- Functions that control the skill's behavior ------------------


def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the Alexa TV IR Remote. Please tell me what to do, " \
                    "for example you can say, 'change to channel 4' or 'mute'."
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "I was unable to understand your request, please try again."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def send_speech_error_to_user():
    card_title = "Error"
    speech_output = "Sorry, I didn't quite catch that, what do you want to do?"
    # Setting this to true ends the session and exits the skill.
    should_end_session = False
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying the Alexa Skills Kit sample. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def end_session_with_message(message):
    card_title = "Session Ended"
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, message, None, should_end_session))


def end_session_with_failed_iot():
    end_session_with_message("Unable to send command to remote.")


def send_iot_request(key_presses):
    print("sending key presses")
    for a in key_presses:
        print(a)

    body = json.dumps(key_presses)

    try:
        iot_client.publish(
            topic=AWS_IOT_PUBLISH_TOPIC,
            qos=0,
            payload=body
        )
        return True
    except Exception as e:
        print("failed to send IOT" + str(e))
        return False


# --------------- Intents ------------------------------------------------------
def change_volume_intent(intent, session):
    """ Increase or decrease the volume. """
    if slot_has_value(intent, 'Volume'):
        val = intent['slots']['Volume']['value']
        if val == "up" or val == "increase":
            send_iot_request(['KEY_VOLUMEUP', 'KEY_VOLUMEUP', 'KEY_VOLUMEUP', 'KEY_VOLUMEUP'])
            return end_session_with_message("Increasing volume")
        elif val == "down" or val == "decrease":
            send_iot_request(['KEY_VOLUMEDOWN', 'KEY_VOLUMEDOWN', 'KEY_VOLUMEDOWN', 'KEY_VOLUMEDOWN'])
            return end_session_with_message("Decreasing volume")
    else:
        print("volume intent received without slot populated")
        return send_speech_error_to_user()


def mute_intent(intent, session):
    """ Mute the television. """
    send_iot_request(['KEY_MUTE'])
    return end_session_with_message("Pressing the mute button!")


def change_power_intent(intent, session):
    """ Press the power button. """
    if slot_has_value(intent, 'PowerChange'):
        send_iot_request(['KEY_POWER'])
        return end_session_with_message("Pressing the power button")
    else:
        print("power intent received without slot populated")
        return send_speech_error_to_user()


def change_channel_intent(intent, session):
    """ Changes the channel based on a Numeric or Word slot. """
    if slot_has_value(intent, 'Channel'):
        channel = intent['slots']['Channel']['value']
        if channel.isdigit():
            numerical_channel = int(channel)
        else:
            numerical_channel = channel_to_numerical(intent['slots']['Channel']['value'])
    else:
        print("channel intent received without slot populated")
        return send_speech_error_to_user()

    # Check the numerical_channel is indeed numeric and > 0
    if not isinstance(numerical_channel, ( int, long ) ) or numerical_channel < 0:
        print("channel invalid: " + str(numerical_channel))
        return send_speech_error_to_user()

    # Send a request for this numerical channel, convert a number to KEY_X
    key_presses = []
    string_number = str(numerical_channel)
    for a in string_number:
        key_presses.append('KEY_' + a)

    # Send key press array to IOT
    if send_iot_request(key_presses):
        # Return nicely
        return end_session_with_message("Changing channel.")
    else:
        # Return with IOT message
        return end_session_with_failed_iot()


# --------------- Events ------------------
def on_session_started(session_started_request, session):
    """ Called when the session starts """
    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "ChannelChangeIntent":
        return change_channel_intent(intent, session)
    elif intent_name == "PowerIntent":
        return change_power_intent(intent, session)
    elif intent_name == "VolumeChangeIntent":
        return change_volume_intent(intent, session)
    elif intent_name == "VolumeMuteIntent":
        return mute_intent(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
