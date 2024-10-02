from django.shortcuts import render, redirect
from .models import Conversation, Session
from .forms import GPTModelForm, ApiKeyForm, ConversationForm
import openai
from datetime import datetime
from django.conf import settings


# Utility function to set OpenAI API key
def set_openai_api_key():
    openai.api_key = settings.OPENAI_API_KEY


# Function to handle GPT chat interaction using the new API (v1.0.0+)
def chat_with_gpt(messages, model="gpt-4"):
    set_openai_api_key()

    # Prepare the conversation messages for the chat completion API
    conversation = [{"role": msg['role'], "content": msg['content']} for msg in messages]

    # Use the new chat completions API
    response = openai.chat.completions.create(
        model=model,
        messages=conversation,
        max_tokens=150
    )

    # Extract the assistant's response from the API
    gpt_response = response.choices[0].message.content.strip()

    return gpt_response


# View for handling the chat interface
def chat_view(request):
    # Retrieve the selected GPT model from the session
    gpt_model = request.session.get('gpt_model')
    if not gpt_model:
        return redirect('choose_gpt_model')

    set_openai_api_key()

    # Check if a session exists; if not, create it without a name initially
    session_id = request.session.get('session_id', None)
    if session_id is None:
        session_id = datetime.now().strftime("%Y%m%d%H%M%S")
        request.session['session_id'] = session_id
        new_session = Session(session_id=session_id, name='')  # No name initially
        new_session.save()

    session = Session.objects.get(session_id=session_id)
    conversation_history = Conversation.objects.filter(session=session).order_by('timestamp')
    messages = [{"role": convo.role, "content": convo.content} for convo in conversation_history]

    if not messages:
        messages.append({"role": "system", "content": "You are a helpful assistant."})

    if request.method == 'POST' and 'send_prompt' in request.POST:
        form = ConversationForm(request.POST)
        if form.is_valid():
            user_prompt = form.cleaned_data['prompt']
            user_message = Conversation(session=session, role="user", content=user_prompt)
            user_message.save()
            messages.append({"role": "user", "content": user_prompt})

            # If the session doesn't have a name yet, generate it now
            if session.name == '':
                session_name = generate_session_name()
                session.name = session_name
                session.save()

            # Get GPT response
            gpt_response = chat_with_gpt(messages, model=gpt_model)
            assistant_message = Conversation(session=session, role="assistant", content=gpt_response)
            assistant_message.save()
            messages.append({"role": "assistant", "content": gpt_response})

            return redirect('chat')
    else:
        form = ConversationForm()

    return render(request, 'conversation/chat.html', {
        'form': form,
        'conversation_history': conversation_history,
        'session': session,
    })


# View for loading existing sessions
def load_session_view(request):
    # Display all available sessions
    sessions = Session.objects.all()

    if request.method == 'POST':
        session_id = request.POST.get('session_id')
        request.session['session_id'] = session_id
        return redirect('chat')

    return render(request, 'conversation/load_session.html', {
        'sessions': sessions
    })


# Function to generate a session name using GPT
def generate_session_name():
    set_openai_api_key()

    # Create a prompt to generate a unique session name
    prompt = "Create a unique and creative name for a chat session."

    # Request GPT to generate a session name using the chat completions API
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=10
    )

    # Extract the generated session name from the response
    session_name = response.choices[0].message.content.strip()

    return session_name


# View for choosing GPT models
def choose_gpt_model(request):
    # Fetch available models from OpenAI API
    available_models = get_available_gpt_models()

    if request.method == 'POST':
        form = GPTModelForm(request.POST, available_models=available_models)
        if form.is_valid():
            # Store the selected model in the session
            request.session['gpt_model'] = form.cleaned_data['model']
            return redirect('chat')
    else:
        form = GPTModelForm(available_models=available_models)

    return render(request, 'conversation/choose_model.html', {'form': form})


# Fetch available GPT models from OpenAI API
def get_available_gpt_models():
    set_openai_api_key()

    # Fetch all available models using the new API
    models_list = openai.models.list()

    # Retrieve the IDs of models that are compatible with chat, e.g., gpt-4, gpt-3.5-turbo
    models = [model.id for model in models_list.data if 'gpt' in model.id]

    return models


# View for setting the OpenAI API key via a form
def set_api_key(request):
    if request.method == 'POST':
        form = ApiKeyForm(request.POST)
        if form.is_valid():
            # Store the API key in the session
            request.session['api_key'] = form.cleaned_data['api_key']
            return redirect('chat')
    else:
        form = ApiKeyForm()

    return render(request, 'conversation/api_key.html', {'form': form})


# View to start a new session (clears the current session data)
def new_session_view(request):
    # Clear the session_id from the session
    if 'session_id' in request.session:
        del request.session['session_id']

    # Optionally clear the GPT model as well if needed
    # if 'gpt_model' in request.session:
    #     del request.session['gpt_model']

    # Redirect to model selection or directly to the chat page for a new session
    return redirect('choose_gpt_model')

