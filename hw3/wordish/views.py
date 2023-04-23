from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello world!")


# The action for the 'greet_get' path.
def greet_post(request):
    if request.method == 'GET':
        return render(request, 'wordish/greet-post-form.html')

    # Creates a context dictionary (map) to send data to the templated HTML file
    context = {}

    # The 'name' parameter is not present.  Display error message (using a template)
    if 'firstname' not in request.POST:
        context['message'] = 'Parameter "firstname" was not sent in the POST request'
        return render(request, 'wordish/greet-post-message.html', context)

    # The 'name' parameter is present so add it to context and render templated HTML file
    context['person_name'] = request.POST['firstname']
    return render(request, 'wordish/greet-post-hello.html', context)

# The action for the 'start_page' path.
def start_action(request):
    # Creates a context dictionary (map) to send data to the templated HTML file
    # context = {}

    if request.method == 'GET':
        context = {"message": "Welcome to Wordish"}
        return render(request, 'wordish/start.html', context)

    try:
        target = _process_param(request.POST, 'target')
        context = _compute_context(target, '')
        return render(request, "wordish/game.html", context)
    except Exception as e:
        context = {"message": "Invalid input: " + str(e)}
        return render(request, "wordish/start.html", context)

def guess_action(request):
    if request.method == "GET":
        context = {"message": "You're hacking.  Try again!"}
        return render(request, "wordish/start.html", context)

    try:
        target = _process_param(request.POST, "target")
        old_guesses = _process_old_guesses(request.POST)
    except Exception as e:
        return render(request, "wordish/start.html", {"message": "Fatal error: " + str(e)})

    try:
        new_guess = _process_param(request.POST, "new-guess")
        old_guesses.append(new_guess)
        context = _compute_context(target, old_guesses)
    except Exception as e:
        context = _compute_context(target, old_guesses)
        context["status"] = "Invalid input:" + str(e)

    return render(request, "wordish/game.html", context)

def _process_param(request_method, param):
    if param not in request_method:
        raise Exception

    text = request_method[param]
    if len(text) != 5:
        raise Exception('Input length is not equal to 5.')

    for i in range(len(text)):
        if not ((text[i] >= 'a' and text[i] <= 'z') or (text[i] >= 'A' and text[i] <= 'Z')):
            raise Exception('Please enter letters.')

    return text.upper()

def _compute_context(target, guesses):
    matrix = []

    # Default cells
    for row in range(6):
        matrix.append([])
        for column in range(5):
            cell = {
                "id": "cell_" + str(row) + "_" + str(column), 
                "letter": "", 
                "color": 'lightgrey'
            }
            matrix[row].append(cell)
    
    color, status = _update_cell_color_and_status(target, guesses)

    for row in range(len(guesses)):
        for column in range(5):
            cell = {
                "id": "cell_" + str(row) + "_" + str(column), 
                "letter": guesses[row][column], 
                "color": color[row][column]
            }
            matrix[row][column] = cell

    status = status
    context = {
        "status": status,
        "matrix": matrix,
        "target": target,
        "old_guesses": ',' .join(guesses),
    }
    return context

def _process_old_guesses(request_method):
    if 'old-guesses' in request_method:
        old_guesses = request_method['old-guesses'].split(',')
        if old_guesses[0] == '':
            old_guesses = old_guesses[1:]
        for guess in old_guesses:
            if len(guess) != 5:
                raise Exception('Input length is not equal to 5.')

            for i in range(len(guess)):
                if not ((guess[i] >= 'a' and guess[i] <= 'z') or (guess[i] >= 'A' and guess[i] <= 'Z')):
                    raise Exception('Please enter letters.')
    else:
        old_guesses = []
    return old_guesses

def _update_cell_color_and_status(target, guesses):
    color = []
    status = "Welcome to Wordish! Start!"
    guess_count = len(guesses)
    if guesses == '':
        return color, status

    for row in range(len(guesses)):
        color.append([])
        count = {}
        guessText = guesses[row]

        for i in range(5):
            color[row].append('grey')
            if target[i] in count:
                count[target[i]] += 1
            else:
                count[target[i]] = 1

        correctLetter = 0

        for i in range(5):
            if guessText[i] == target[i] and count[guessText[i]] > 0:
                correctLetter += 1
                count[guessText[i]] -= 1
                color[row][i] = 'green'
                continue
        
        for i in range(5):
            for j in range(5):
                if guessText[i] == target[j] and j != i and count[guessText[i]] > 0 and color[row][i] != 'green':
                    count[guessText[i]] -= 1
                    color[row][i] = 'yellow'
                    break

        if correctLetter == 5:
            status = "win~"
            return color, status

    if guess_count >= 6 and correctLetter != 5:
        status = "You lose."
        return color, status

    if guess_count > 0 and guesses[0] != '':    
        status = "successful input"
    return color, status