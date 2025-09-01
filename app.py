from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Dicionário para "salvar" o estado da conversa de cada usuário (simulado)
# Em um app real, isso seria um banco de dados (Redis, etc.)
user_sessions = {}


@app.route('/')
def home():
    # Reinicia a sessão ao carregar a página
    user_sessions.clear()
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message').lower()
    session_id = request.remote_addr  # Simples identificador de usuário pelo IP

    # Se a sessão não existe, cria uma nova
    if session_id not in user_sessions:
        user_sessions[session_id] = {'step': 'inicio'}

    current_step = user_sessions[session_id]['step']
    bot_responses = []

    # --- LÓGICA DO FLUXO DE AGENDAMENTO ---

    if current_step == 'inicio':
        if user_message == '1' or "agendar" in user_message:
            bot_responses.append("Ótima escolha! Para qual dia você gostaria de agendar?")
            bot_responses.append(
                "Estes são os próximos dias disponíveis:\n1️⃣ Terça-feira (02/09)\n2️⃣ Quarta-feira (03/09)\n3️⃣ Sexta-feira (05/09)")
            user_sessions[session_id]['step'] = 'escolher_dia'
        elif user_message == '2' or "atendente" in user_message:
            bot_responses.append("Ok, um momento que vou te transferir para um de nossos atendentes.")
            user_sessions[session_id]['step'] = 'fim'  # Finaliza o fluxo do bot
        else:
            bot_responses.append("Olá! 👋 Seja bem-vindo(a). Como posso ajudar?")
            bot_responses.append("1️⃣ Agendar consulta\n2️⃣ Falar com um atendente")

    elif current_step == 'escolher_dia':
        # Mapeia a escolha para o dia da semana
        dias = {'1': 'Terça-feira (02/09)', '2': 'Quarta-feira (03/09)', '3': 'Sexta-feira (05/09)'}
        if user_message in dias:
            dia_escolhido = dias[user_message]
            user_sessions[session_id]['dia'] = dia_escolhido  # Salva o dia na sessão
            bot_responses.append(f"Perfeito! Para {dia_escolhido}, tenho os seguintes horários livres:")
            bot_responses.append("1️⃣ 09:00h\n2️⃣ 11:00h\n3️⃣ 14:30h")
            user_sessions[session_id]['step'] = 'escolher_horario'
        else:
            bot_responses.append("Opção inválida. Por favor, escolha um dos dias disponíveis (1, 2 ou 3).")

    elif current_step == 'escolher_horario':
        horarios = {'1': '09:00h', '2': '11:00h', '3': '14:30h'}
        if user_message in horarios:
            horario_escolhido = horarios[user_message]
            dia_escolhido = user_sessions[session_id]['dia']
            user_sessions[session_id]['horario'] = horario_escolhido  # Salva o horário
            bot_responses.append(
                f"Excelente! Para confirmar, seu agendamento é para <strong>{dia_escolhido} às {horario_escolhido}</strong>. Está correto?")
            bot_responses.append("1️⃣ Sim, confirmar\n2️⃣ Não, escolher outro horário")
            user_sessions[session_id]['step'] = 'confirmar'
        else:
            bot_responses.append("Opção inválida. Por favor, escolha um dos horários disponíveis (1, 2 ou 3).")

    elif current_step == 'confirmar':
        if user_message == '1' or "sim" in user_message:
            dia = user_sessions[session_id]['dia']
            horario = user_sessions[session_id]['horario']
            bot_responses.append(
                f"✅ <strong>Agendamento Concluído!</strong>\nSua consulta está marcada para {dia}, às {horario}. Enviaremos um lembrete um dia antes. Obrigado!")
            user_sessions[session_id]['step'] = 'fim'
        elif user_message == '2' or "não" in user_message:
            bot_responses.append("Sem problemas. Vamos tentar novamente.")
            bot_responses.append(
                "Estes são os próximos dias disponíveis:\n1️⃣ Terça-feira (02/09)\n2️⃣ Quarta-feira (03/09)\n3️⃣ Sexta-feira (05/09)")
            user_sessions[session_id]['step'] = 'escolher_dia'
        else:
            bot_responses.append("Por favor, responda com '1' para sim ou '2' para não.")

    return jsonify({'responses': bot_responses})

if __name__ == '__main__':
    app.run(debug=True)