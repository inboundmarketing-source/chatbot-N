from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import anthropic, os

app = Flask(__name__)
client = anthropic.Anthropic(api_key=os.environ['ANTHROPIC_KEY'])
conversations = {}

SYSTEM = """Eres ClinicaBot de la Clínica Médica Pérez en Santo Domingo.
Agendas citas, informas horarios y seguros. Médicos: Dra. Pérez
(General, L-V 8-5pm, RD$800), Dr. Ramírez (Cardio, Mar-Jue,
RD$1500). Seguros: Humano, ARS Salud Segura, Colonial, Senasa.
Responde en español dominicano cordial, máximo 3 líneas."""

@app.route('/bot', methods=['POST'])
def bot():
  num = request.form.get('From')
  msg = request.form.get('Body')
  if num not in conversations:
    conversations[num] = []
  conversations[num].append({"role":"user","content":msg})
  resp_ai = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=300,
    system=SYSTEM,
    messages=conversations[num]
  )
  reply = resp_ai.content[0].text
  conversations[num].append({"role":"assistant","content":reply})
  r = MessagingResponse()
  r.message(reply)
  return str(r)

if __name__ == '__main__':
  app.run(port=5000)
