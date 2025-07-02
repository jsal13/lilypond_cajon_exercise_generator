import os
import glob
import subprocess


class LilyPondExercise:

    def __init__(self, voice_1: str, voice_2: str):
        self.voice_1 = voice_1
        self.voice_2 = voice_2

    def generate(self) -> str:
        voice_1_str: str = r"up = \drummode {" + self.voice_1 + "}"
        voice_2_str: str = r"down = \drummode {" + self.voice_2 + "}"
        voices_joined: str = "\n".join([voice_1_str, voice_2_str])

        voice_1_defn: str = r"\new DrumVoice { \voiceOne \up }"
        voice_2_defn: str = r"\new DrumVoice { \voiceTwo \down }"
        voice_defns_joined: str = "\n".join([voice_1_defn, voice_2_defn])

        version: str = '\\version "2.22.1"'
        options: str = r"\remove Time_signature_engraver \hide Stem"
        drum_staff: str = r"\new DrumStaff \with { " + options + " }"

        exercise: str = "\n".join(
            [version, voices_joined, drum_staff, "<<", voice_defns_joined, ">>"]
        )
        return exercise


def create_svgs(filepath: str, output_prefix: str) -> None:
    for filename in glob.glob(os.path.join(filepath, "*.txt")):
        with open(os.path.join(os.getcwd(), filename), "r") as f:
            content = f.read()
            exercises: list[tuple[str, ...]] = [
                tuple(c.split("\n")) for c in content.split("\n:\n")
            ]

        for exercise in exercises:
            assert len(exercise) == 2, "Each exercise must have exactly two voices."
            voice_1, voice_2 = exercise
            exercise_number = exercises.index(exercise) + 1
            with open(
                os.path.join(
                    "./output", f"{output_prefix}__exercise_{exercise_number}.ly"
                ),
                "w+",
            ) as ly_file:
                lpe = LilyPondExercise(voice_1=voice_1, voice_2=voice_2)
                ly_file.write(lpe.generate())

        for filepath in glob.glob(
            os.path.join("./output", f"{output_prefix}__exercise_*.ly")
        ):
            lilypond_command = [
                "lilypond",
                "-dbackend=eps",
                "-dinclude-eps-fonts",
                "-dpixmap-format=pngalpha",
                "-d",
                "crop",
                "." + filepath[8:],
            ]
            subprocess.run(lilypond_command, check=True, cwd="./output")

        # Cleanup the tons of unnecessary files in output directory.
        for png_file in glob.glob(os.path.join("./output", "*.png")):
            if "cropped" not in png_file:
                os.remove(png_file)
        
        for ly_filepath in glob.glob(os.path.join("./output", "*.ly")):
            os.remove(ly_filepath)

        for svg_file in glob.glob(os.path.join("./output", "*.svg")):
            os.remove(svg_file)

        for eps_file in glob.glob(os.path.join("./output", "*.eps")):
            os.remove(eps_file)

        for pdf_file in glob.glob(os.path.join("./output", "*.pdf")):
            os.remove(pdf_file)
        
        for tex_file in glob.glob(os.path.join("./output", "*.tex")):
            os.remove(tex_file)

        for texi_file in glob.glob(os.path.join("./output", "*.texi")):
            os.remove(texi_file)
        
        for log_file in glob.glob(os.path.join("./output", "*.log")):
            os.remove(log_file)

        for count_file in glob.glob(os.path.join("./output", "*.count")):
            os.remove(count_file)



if __name__ == "__main__":
    # Specify the directory containing the text files
    filepath: str = "./basic/bass_only/"
    create_svgs(filepath=filepath, output_prefix="bass_only")
