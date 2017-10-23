'use strict';
var Alexa = require('alexa-sdk');
var request = require("request");
var firebase = require('firebase');
var config = require('./config');
const APP_ID = "amzn1.ask.skill.54bd94d9-34d5-47a1-8b98-54e403c97dc3";  // Your app ID.
var slotType = '';
var nameValue = '';

firebase.initializeApp({
    serviceAccount: config,
    databaseURL: "https://atom-pet.firebaseio.com/"
});

var database = firebase.database();

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

function doTricks(callback) {
    // If we wanted to initialize the session to have some attributes we could add those here.
    const sessionAttributes = {};
    var speechOutput = "Doing mad tricks right now"
    const cardTitle = 'Tricks';
    // getJSON(function(data) {
    //     if (data != "ERROR") {
    //         var speechOutput = data;
    //     }
    //     const repromptText = data;
    //     const shouldEndSession = false;
    //     callback(sessionAttributes,
    //         buildSpeechletResponse(cardTitle, speechOutput, repromptText, shouldEndSession));
    // })
    var speechOutput = 'Here is where we say what trick is happening';
    const repromptText = 'Here is where we say what trick is happening';
    const shouldEndSession = false;   
    callback(sessionAttributes,
        buildSpeechletResponse(cardTitle, speechOutput, repromptText, shouldEndSession));
}

//finds the specific slot requested, and then builds off of that
function comeToMe(intent, session, callback) {
    const cardTitle = 'Come Here';
    const nameSlot = intent.slots.Names; //get the necessary slot information
    let repromptText = 'doggo is on his way';
    let sessionAttributes = {};
    const shouldEndSession = false;
    let speechOutput = 'you know this doggo is coming to you';
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
        
        let today = new Date();
        let time = today.toLocaleString();
        database.ref().push({
            timestamp: time
        },() => { 
            repromptText = time;
        });
        //Then call a get request now that slotType is saved. Then get your corresponding data back
        // getJSONSpecific(function(data) {
        //     if (data != "ERROR") {
        //         if()){
        //             var speechOutput = ;
        //             const repromptText = ;
        //         }
        //         else{
        //             var speechOutput =;
        //             const repromptText = ;
        //         }
        //     }
        //     else {
        //         speechOutput = "I'm not sure what you said, can you please repeat that?";
        //         repromptText = "Please tell Atom who you would like him to go to";
        //     }
            callback(sessionAttributes,
                buildSpeechletResponse(cardTitle, speechOutput, repromptText, shouldEndSession));
        // })
    }
    else {
        speechOutput = "I'm not sure what you said, can you please repeat that?";
        repromptText = "Please tell Atom who you would like him to go to";
        callback(sessionAttributes,
 buildSpeechletResponse(cardTitle, speechOutput, repromptText, shouldEndSession));
    }         
}

function cleanUp(callback) {
    const sessionAttributes = {};
    var speechOutput = "reached clean up"
    const cardTitle = 'Clean Up';
    const repromptText = "reached clean up";
    // getJSONSpecific(function(data) {
    //     if (data != "ERROR") {
    //         if(){
    //             var speechOutput =;
    //             const repromptText = ;
    //         }
    //         else{
    //             var speechOutput = ;
    //             const repromptText =;
    //         }
    //     }
    //     else {
    //         speechOutput = "I'm not sure what you said, can you please repeat that?";
    //         repromptText = "Please tell Atom who you would like him to go to";
    //     }
        callback(sessionAttributes,
            buildSpeechletResponse(cardTitle, speechOutput, repromptText, shouldEndSession));
    // })
}

function http() {
    var send = ""
    return send
}

function https() {
    return {
        url: "",
        headers: {
            Authorization : ""
        }
    }
}

function getJSON(callback) {
    // HTTPS request
    request.get(https(), function(error, response, body) {
        var d = JSON.parse(body)
        //this would be whatever necessary information you need to pull out from the JSON
        var result = d.serial
        if (result.length > 0) {
            callback(result)
        } else {
            callback("ERROR")
        }
    })
}
function postJSON(callback) {
    // HTTPS request
    request.post(https(), function(error, response, body) {
        var d = JSON.parse(body)
        //this would be whatever necessary information you need to pull out from the JSON
        var result = d.serial
        if (result.length > 0) {
            callback(result)
        } else {
            callback("ERROR")
        }
    })
}

function getJSONSpecific(callback) {
    request.get(http(), function(error, response, body) {
        var raw = JSON.parse(body)
        //get the necessary information from the JSON
        var result = raw[slotType]
        if (result > 0) {
            callback(result);
        } else {
            callback("ERROR");
        }
    })
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
function onIntent(intentRequest, session, callback) {
    console.log(`onIntent requestId=${intentRequest.requestId}, sessionId=${session.sessionId}`);

    const intent = intentRequest.intent;
    const intentName = intentRequest.intent.name;

    // Dispatch to your skill's intent handlers
    if (intentName === 'AMAZON.HelpIntent') {
        getWelcomeResponse(callback);
    } else if (intentName === 'Tricks') {
        doTricks(callback);
    } else if (intentName === 'ComeToMe') {
        comeToMe(intent, session, callback);
    } else if (intentName === 'CleanUp') {
        cleanUp(callback);
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

        /**
         * Uncomment this if statement and populate with your skill's application ID to
         * prevent someone else from configuring a skill that sends requests to this function.
         */
        /*
        if (event.session.application.applicationId !== 'amzn1.echo-sdk-ams.app.[unique-value-here]') {
             callback('Invalid Application ID');
        }
        */

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
                event.session,
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
