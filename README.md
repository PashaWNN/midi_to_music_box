---
title: MIDI to music box
emoji: 🎶🎶
colorFrom: red
colorTo: yellow
sdk: gradio
sdk_version: "4.36.1"
app_file: app.py
pinned: false
---

# Music Box Movement Drum Generator

Have you ever wondered if you can create a melody for the music box by yourself? It is made possible with this app.
All you need is a typical music box, an SLA 3D printer and this app.

App on HuggingFace: [MIDI to Music Box](https://huggingface.co/spaces/PashaWNN/midi_to_music_box)

## Custom Music Box Step-by-step guide

### Step 1. Get a music box movement mechanism.

This script is designed for the most popular mechanism, like the one shown in the picture below.
![Mechanism reference](https://raw.githubusercontent.com/PashaWNN/midi_to_music_box/main/media/mechanism.webp)

### Step 2. Write down the notes from your music box

You need to unscrew the original drum from your music box mechanism and pluck the comb teeth one by one, writing down
the notes.
You can use any tuner mobile or web app to check the notes using a microphone.
This is necessary because music boxes tend to have different tuning. Also, it is common to have some notes appearing
twice on different comb teeth.

### Step 3. Compose a music track.

You can use any software that is capable of exporting melodies to MIDI format. For example, you can compose music using
the [MusicBoxManiacs website](http://musicboxmaniacs.com/).
There are some limitations to the composed melody:

1. All notes and pauses between them must be of the same length. If that is not the case, this script could work
   incorrectly. Nevertheless, different note lengths do not make sense for a music box.
2. Music boxes are not able to play repetitive notes positioned too close to each other. This can be partially resolved
   when the note is duplicated on your music box comb. The script will automatically use different comb teeth each time
   the note is played.
3. If the composition is too long, there will not be enough space on the drum to play it normally. It is recommended to
   have no more than 100 notes in length.

### Step 4. Generate an STL

Once your composition is completed and saved as a `.mid` file, you are all set to generate an STL.

Visit the app here: [MIDI to Music Box](https://huggingface.co/spaces/PashaWNN/midi_to_music_box).
You will be prompted to enter the MIDI filename and the available notes.

The script will show an error message if some notes from the MIDI file are missing on your music box. 
If everything is fine, you will see the model and be able to download it by clicking tiny download button in the corner.

### Step 5. Print the model

Once you have generated the model, you can print it out. It is recommended to use Tough Resin to do that. The model
should be printed as is, without reorienting or supporting. Make sure you do not overexpose burn-in layers too much as
you will have to get rid of an elephant foot and cut it so the conical hole in the middle corresponds with the screw on
the music box.
Detach the gear from the original drum and attach it to your brand-new drum. Screw it back to the music box and test it.

### Troubleshooting

**Problem**: The music is playing too slow/too fast.
**Solution**: Try moving the governor on the music box higher/lower. Also, experiment with the melody itself by placing
notes closer/wider to each other.
**Problem**: There is no delay after the end of playback
**Solution**: Add some space before the first note in the composition.
**Problem**: I can not access the app
**Solution**: You can try contacting me or running it locally. To run it locally you will need Docker installed on your machine. Clone the repository and run `docker build -t gradio-app . && docker run -p 7860:7860 gradio-app` in its root. Then just open the app [in your browser](http://127.0.0.1:7860).
**Problem**: I use command line interface version of the script, and it fails to find OpenSCAD
**Solution**: If you have OpenSCAD installed, but it is not found by the script, you have to options: either you need to add OpenSCAD to your PATH or you can just specify `OPENSCAD_BINARY` environment variable with the path to the OpenSCAD binary.


### All ways to run it.

1. Go to the HuggingFace: [MIDI to Music Box](https://huggingface.co/spaces/PashaWNN/midi_to_music_box);
2. Run it using Docker: `docker build -t gradio-app . && docker run -p 7860:7860 gradio-app` then go to `http://127.0.0.1:7860` in the browser;
3. Run the web app without Docker: `pip install -r requirements.txt && python3 app.py` then go to `http://127.0.0.1:7860` in the browser;
4. Run it using CLI: `pip install -r requirements.txt && python3 main.py`. It prompts you for main options, and you can also check out `python3 main.py --help` to see available command line arguments.
