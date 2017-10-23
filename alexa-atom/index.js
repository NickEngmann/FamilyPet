'use strict';
var Alexa = require('alexa-sdk');
var firebase = require('firebase');
const APP_ID = "amzn1.ask.skill.54bd94d9-34d5-47a1-8b98-54e403c97dc3";  // Your app ID.
var slotType = '';
var nameValue = '';

/*
The way this code works is by making requests to firebase, updating the status of Atom so that atom can 
execute the appropriate functions.
It does this by:
*/

// --------------- Helpers that build all of the responses -----------------------

function buildSpeechletResponse(title, output, repromptText, shouldEndSession) {
    return {
        outputSpeech: {
            type: 'PlainText',
            text: output,
        },
        card: {
            type: 'Simple',
            title: `SessionSpeechlet - ${title}`,
            content: `SessionSpeechlet - ${output}`,
        },
        reprompt: {
            outputSpeech: {
                type: 'PlainText',
                text: repromptText,
            },
        },
        shouldEndSession,
    };
}

function buildResponse(sessionAttributes, speechletResponse) {
    return {
        version: '1.0',
        sessionAttributes,
        response: speechletResponse,
    };
}

// --------------- Functions that control the skill's behavior -----------------------

function getWelcomeResponse(callback) {
    // If we wanted to initialize the session to have some attributes we could add those here.
    const sessionAttributes = {};
    const cardTitle = 'Welcome';
    const speechOutput = 'Atom is awake. ' +
        'What do you want him to do?';
    // If the user either does not reply to the welcome message or says something that is not
    // understood, they will be prompted again with this text.
    const repromptText = 'Atom is awake, ' +
        'What do you want him to do';
    const shouldEndSession = false;

    callback(sessionAttributes,
        buildSpeechletResponse(cardTitle, speechOutput, repromptText, shouldEndSession));
}

function doTricks(callback, database) {
    const cardTitle = 'Tricks';
    let repromptText = 'Atom is doing tricks';
    let sessionAttributes = {};
    const shouldEndSession = false;
    let speechOutput = 'Those some mad tricks yo';

    var today = new Date();
    let time = today.toLocaleString();
    database.ref("status/").update({
        command: 'tricks',
        timestamp: time
    },() => { 
        callback(sessionAttributes,
            buildSpeechletResponse(cardTitle, speechOutput, repromptText, shouldEndSession));
    });
}

function comeToMe(intent, session, callback, database) {
    const cardTitle = 'Come Here';
    const nameSlot = intent.slots.Names; //get the necessary slot information
    let repromptText = 'Atom is on his way';
    let sessionAttributes = {};
    const shouldEndSession = false;
    let speechOutput = '';
    //finds the specific slot requested, and then builds off of that
    if (nameSlot) {
        //if nameSlot exists, find out which name Slot was mentioned, and create the specific slotType for that nameSlot
        nameValue = nameSlot.value;
        if (nameValue == 'Daniel'){
            slotType = 'Daniel'
        }
        else if (nameValue == 'Danny'){
            slotType = 'Danny'
        }
        else if (nameValue == 'Nick'){
            slotType = 'Nick'
        }
        else if (nameValue == 'Nicky'){
            slotType = 'Nicky'
        }
        else if (nameValue == 'Swagster'){
            slotType = 'Swagster'
        }
        var today = new Date();
        let time = today.toLocaleString();
        speechOutput = 'Atom is going to '+ nameValue;
        database.ref("status/").update({
            command: 'comeToMe',
            timestamp: time,
            user: slotType
        },() => { 
            callback(sessionAttributes,
                buildSpeechletResponse(cardTitle, speechOutput, repromptText, shouldEndSession));
        });
    }
    else {
        speechOutput = "I'm not sure what you said, can you please repeat that?";
        repromptText = "Please tell Atom who you would like him to go to";
        callback(sessionAttributes,
            buildSpeechletResponse(cardTitle, speechOutput, repromptText, shouldEndSession));
    }         
}

function cleanUp(callback, database) {
    const cardTitle = 'Clean Up';
    let repromptText = 'Atom is cleaning up';
    let sessionAttributes = {};
    const shouldEndSession = false;
    let speechOutput = 'Atom is cleaning up';

    var today = new Date();
    let time = today.toLocaleString();
    database.ref("status/").update({
        command: 'cleanUp',
        timestamp: time
    },() => { 
        repromptText = time;
        callback(sessionAttributes,
            buildSpeechletResponse(cardTitle, speechOutput, repromptText, shouldEndSession));
    });
}

function handleSessionEndRequest(callback) {
    //Saying Goodbye once a session ends
    const cardTitle = 'Session Ended';
    const speechOutput = 'Atom is tired and is going to go back to sleep';
    // Setting this to true ends the session and exits the skill.
    const shouldEndSession = true;

    callback({}, buildSpeechletResponse(cardTitle, speechOutput, null, shouldEndSession));
}


// --------------- Events -----------------------

/**
 * Called when the session starts.
 */
function onSessionStarted(sessionStartedRequest, session) {
    console.log(`onSessionStarted requestId=${sessionStartedRequest.requestId}, sessionId=${session.sessionId}`);
}

/**
 * Called when the user launches the skill without specifying what they want.
 */
function onLaunch(launchRequest, session, callback) {
    console.log(`onLaunch requestId=${launchRequest.requestId}, sessionId=${session.sessionId}`);

    // Dispatch to your skill's launch.
    getWelcomeResponse(callback);
}

/**
 * Called when the user specifies an intent for this skill.
 */
function onIntent(intentRequest, session, database, callback) {
    console.log(`onIntent requestId=${intentRequest.requestId}, sessionId=${session.sessionId}`);

    const intent = intentRequest.intent;
    const intentName = intentRequest.intent.name;

    // Dispatch to your skill's intent handlers
    if (intentName === 'AMAZON.HelpIntent') {
        getWelcomeResponse(callback);
    } else if (intentName === 'Tricks') {
        doTricks(callback, database);
    } else if (intentName === 'ComeToMe') {
        comeToMe(intent, session, callback, database);
    } else if (intentName === 'CleanUp') {
        cleanUp(callback, database);
    } else if (intentName === 'AMAZON.StopIntent' || intentName === 'AMAZON.CancelIntent') {
        handleSessionEndRequest(callback);
    } else {
        throw new Error('Invalid intent');
    }
}

/**
 * Called when the user ends the session.
 * Is not called when the skill returns shouldEndSession=true.
 */
function onSessionEnded(sessionEndedRequest, session) {
    console.log(`onSessionEnded requestId=${sessionEndedRequest.requestId}, sessionId=${session.sessionId}`);
    // Add cleanup logic here
}

// --------------- Main handler -----------------------

// Route the incoming request based on type (LaunchRequest, IntentRequest,
// etc.) The JSON body of the request is provided in the event parameter.
exports.handler = (event, context, callback) => {
    try {
        console.log(`event.session.application.applicationId=${event.session.application.applicationId}`);

        context.callbackWaitsForEmptyEventLoop = false;  //<---Important
        var config = require('./config.json');     

        if(firebase.apps.length == 0) {   // <---Important!!! In lambda, it will cause double initialization.
            firebase.initializeApp(config);
        }
        var database = firebase.database();
        if (event.session.new) {
            onSessionStarted({ requestId: event.request.requestId }, event.session);
        }

        if (event.request.type === 'LaunchRequest') {
            onLaunch(event.request,
                event.session,
                (sessionAttributes, speechletResponse) => {
                    callback(null, buildResponse(sessionAttributes, speechletResponse));
                });
        } else if (event.request.type === 'IntentRequest') {
            onIntent(event.request,
                event.session, database,
                (sessionAttributes, speechletResponse) => {
                    callback(null, buildResponse(sessionAttributes, speechletResponse));
                });
        } else if (event.request.type === 'SessionEndedRequest') {
            onSessionEnded(event.request, event.session);
            callback();
        }
    } catch (err) {
        callback(err);
    }
};
