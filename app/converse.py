import random

# handles small talk
def handle_convo(command):
    response = 'I gotta tell you, I was always like, "Tracey, this doesn\'t make any sense," and she was like, "Words, words, words and some numbers." But she did it.'

    #define terms
    intro_terms = ["who are you", "tell me about you", "wiseguy"]
    hello_terms = ["hey", "hi", "what's up", "sup", "hai", "hiya"]
    thanks_terms = ["thanks", "thank you"]

    #define responses
    intro_responses = ["> Hi, I'm Mr Wise Guy. You probably saw me in Goodfellas or Mean Streets or the street. I consider myself semi-retired so am doing this for entertainment. AMA!", ">https://gph.is/1Qxikam"]
    hello_responses = ["> Dude!\n> https://gph.is/1QhIu3O", "> Oh, heyyy", "> What\'s up dog?", "> Hey there, e-friend!", "> You know? I'm real", "> Hey, how can I help?"]
    thanks_responses = ["> https://gph.is/2nKrP3C", "> Don't mention it!"]

    # handle response
    if any(a in command for a in intro_terms):
        response = random.choice(intro_responses)

    elif any(b in command for b in hello_terms):
        response = random.choice(hello_responses)

    elif any(c in command for c in thanks_terms):
        response = random.choice(thanks_responses)

    return response