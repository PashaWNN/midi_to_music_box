# Music Box Movement Drum Generator

Have you ever wondered if you can create a melody for the music box by yourself? It is made possible with this script.
All you need is a typical music box, an SLA 3D printer, and Python installed on your computer.

## Custom Music Box Step-by-step guide

### Step 1. Get a music box movement mechanism.

This script is designed for the most popular mechanism, like the one shown in the picture below.
![Mechanism reference](https://raw.githubusercontent.com/PashaWNN/midi_to_music_box/main/mechanism.webp)

### Step 2. Write down the notes from your music box

You need to unscrew the original drum from your music box mechanism and pluck the comb teeth one by one, writing down
the notes.
You can use any tuner mobile or web app to check the notes using a microphone.
This is necessary because music boxes tend to have different tuning. Also, it is common to have some notes appearing
twice on different comb teeth.
Once you have written the notes down, starting from the left side (near the spring) to the right side near the drum
screw, write them line by line to the file `notes.txt`.

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
Make sure you have installed all the requirements: you need to have Python 3 and OpenSCAD installed, then you need to
install needed Python packages:

```shell
pip install -r requirements.txt
```

When all requirements are installed, run the script `main.py` and pass your file as an argument:

```shell
python3 main.py my_wholesome_melody.mid
```

The script will show an error message if some notes from the MIDI file are missing on your music box (as you have
written notes down to `notes.txt`). If everything is fine, you will see the new file with a `.scad` extension in your
working directory. Open this file in OpenSCAD and use it to render and export an STL file.

### Step 5. Print the model

Once you have generated the model, you can print it out. It is recommended to use Tough Resin to do that. The model
should be printed as is, without reorienting or supporting. Make sure you do not overexpose burn-in layers too much as
you will have to get rid of an elephant foot and cut it so the conical hole in the middle corresponds with the screw on
the music box.
Detach the gear from the original drum and attach it to your brand-new drum. Screw it back to the music box and test it.

### Troubleshooting

**Problem**: Drum pins are too short to pluck the comb teeth.
**Solution**: Try increasing its length in the `scadfile.scad.template`. It is done by altering the `pinHeight`
variable.
**Problem**: Pins seem to not match the comb teeth.
**Solution**: Make sure the printed drum has the correct length. Incorrect length could be caused by wrong print
settings, high shrinkage, or other reasons. Also, make sure your music box has 18 notes. If that is not the case, try
adjusting the `tonesTotalNumber` in the template (not tested).
**Problem**: The music is playing too slow/too fast.
**Solution**: Try moving the governor on the music box higher/lower. Also, experiment with the melody itself by placing
notes closer/wider to each other.
**Problem**: There is no delay after the end of playback
**Solution**: Add some space before the first note in the composition.
