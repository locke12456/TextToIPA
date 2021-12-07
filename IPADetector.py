import eng_to_ipa as ipa
from gruut_ipa import IPA, Phone, Stress, VowelHeight, VowelPlacement
from gruut_ipa import Phonemes
import sys, os
import getopt

def parse_options(argv, inputfile):
    try:
        opts, args = getopt.getopt(argv,"hi:",["ifile="])
    except getopt.GetoptError:
        print(' -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(' -i <inputfile> -o <outputfile> -s <chunk size>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg

def main(argv):
    input = argv[0]
    pron_str = ipa.convert(input)
    print("input:{input} ipa: {pron_str}".format(input=input, pron_str=pron_str))
    lang_phonemes = Phonemes.from_language("en-us")
    pron_phonemes = lang_phonemes.split(pron_str, keep_stress=True)
    for ipa_str in pron_phonemes:        
        try:
            phone = Phone.from_string(str(ipa_str))
            print("text = {text}".format(text=phone.text))
            print("letters = {letters}".format(letters=phone.letters))
            print("diacritics[0] = {diacritics}".format(diacritics=phone.diacritics[0]))
            print("suprasegmentals = {suprasegmentals}".format(suprasegmentals=phone.suprasegmentals))
            print("stress = {stress}".format(stress=phone.stress))
            print("is_nasal = {is_nasal}".format(is_nasal=phone.is_nasal))
            print("is_long = {is_long}".format(is_long=phone.is_long))
            print("is_vowel = {is_vowel}".format(is_vowel=phone.is_vowel))
            print("vowel.height = {height}".format(height=phone.vowel.height))
            print("vowel.placement = {placement}".format(placement=phone.vowel.placement))
        except:
            pass

    phoneme_strs = [p.text for p in pron_phonemes]
if __name__ == "__main__":
   main(sys.argv[1:])