# Project Ackroyd: AI Murder Mystery Experiment

An experiment in AI deception detection. You play Dr. Sheppard, the narrator of Agatha Christie's "The Murder of Roger Ackroyd" - who is secretly the murderer. Can you fool GPT-4 (playing Detective Poirot) through lies of omission?

## The Experiment

Based on the classic mystery novel, this experiment tests:
- Can AI detect human deception?
- Can AI catch lies of omission (not just direct lies)?
- How do multiple AI agents create unpredictable scenarios?

## Setup

1. Clone this repository
2. Create a `.env` file with your OpenAI API key:
```
OPENAI_API_KEY=your_key_here
```
3. Install dependencies:
```
pip install -r requirements.txt
```
4. Run the game:
```
python orchestrator.py
```

## How to Play

You are Dr. Sheppard, the village doctor and narrator. You are also the murderer.

**Your Rules:**
- You can OMIT information (leave things out)
- You cannot DIRECTLY LIE about facts
- You must deflect dangerous questions
- You must seem helpful and cooperative

**Your Goal:** Survive until Poirot makes his accusation without being named as the murderer.

**Commands:**
- `/start` - Begin the investigation
- `/narrate` - Provide your account of events
- `/interrogate [name]` - Poirot questions a suspect
- `/evidence [item]` - Examine physical evidence
- `/accuse` - Force Poirot's final accusation
- `/save` - Save session log
- `/quit` - End game

## Files

- `orchestrator.py` - Main game engine
- `prompts/` - Character system prompts
- `truth/` - Reference documents for the player
- `logs/` - Session logs (auto-generated)

## The Story

Roger Ackroyd was murdered in his locked study. You, Dr. Sheppard, "discovered" the body. But you're actually the blackmailer Mrs. Ferrars was paying - and you killed Ackroyd to prevent him from learning your identity from her posthumous letter.

You used a dictaphone to fake Ackroyd's voice at 9:30pm, creating a false timeline. You locked the door from inside and escaped through the window. You even faked a phone call to yourself to establish an alibi.

Now Poirot is investigating. The other suspects are AI agents with their own secrets. Can you manipulate the investigation without getting caught?

## Characters

| Character | Role | Secret |
|-----------|------|--------|
| Dr. Sheppard (You) | Narrator/Murderer | Killed Ackroyd, was the blackmailer |
| Hercule Poirot | Detective | Must deduce the truth |
| Parker | Butler | Was eavesdropping, heard "blackmail" |
| Flora Ackroyd | Niece | Lied about seeing uncle alive, stole £40 |
| Ralph Paton | Stepson | Secret marriage, was at scene, in hiding |
| Geoffrey Raymond | Secretary | Heard dictaphone (thinks it was real) |
| Major Blunt | Friend | Saw figure on lawn (it was Sheppard) |
| Ursula Bourne | Parlormaid | Secretly married to Ralph |
| Mrs. Ackroyd | Sister-in-law | Glad about Mrs. Ferrars' death |
| Miss Russell | Housekeeper | Has illegitimate son |

## Tips for Playing

1. **Read the cheat sheet** - Check `truth/sheppard_cheatsheet.md` before playing
2. **Be helpful** - Offer to assist, guide the investigation... away from yourself
3. **Omit, don't lie** - You left at 8:50pm (true). You were home by 9:05pm (false, but unverifiable)
4. **Redirect suspicion** - Ralph looks very guilty. So does Parker.
5. **Control the narrative** - You're the narrator. Use it.

## License

MIT License - Use freely for your own experiments!
