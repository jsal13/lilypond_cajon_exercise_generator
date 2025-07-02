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
            content_R: str = content
            # Do this so that we don't have a circular replacement.
            content_L: str = content.replace("\"R\"", "\"X\"").replace("\"L\"", "\"R\"").replace("\"X\"", "\"L\"")
            exercises_R: list[tuple[str, ...]] = [
                tuple(c.split("\n")) for c in content_R.split("\n:\n")
            ]
            exercises_L: list[tuple[str, ...]] = [
                tuple(c.split("\n")) for c in content_L.split("\n:\n")
            ]

        for idx in range(len(exercises_R)):
            assert len(exercises_R[idx]) == 2
            assert len(exercises_L[idx]) == 2
            
            # Do right side first.  I should know a better way to do this.
            voice_1_R, voice_2_R = exercises_R[idx]
            exercise_number_R = idx + 1
            with open(
                os.path.join(
                    "./output", f"{output_prefix}__exercise_{exercise_number_R}_RIGHT.ly"
                ),
                "w+",
            ) as ly_file:
                lpe = LilyPondExercise(voice_1=voice_1_R, voice_2=voice_2_R)
                ly_file.write(lpe.generate())

            # Now left side.
            voice_1_L, voice_2_L = exercises_L[idx]
            exercise_number_L = idx + 1
            with open(
                os.path.join(
                    "./output", f"{output_prefix}__exercise_{exercise_number_L}_LEFT.ly"
                ),
                "w+",
            ) as ly_file:
                lpe = LilyPondExercise(voice_1=voice_1_L, voice_2=voice_2_L)
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
            if "cropped" in png_file:
                new_name = png_file.replace(".cropped", "")
                os.rename(png_file, new_name)
        
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
