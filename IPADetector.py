import eng_to_ipa as ipa
from gruut_ipa import IPA, Phone, Stress, VowelHeight, VowelPlacement
from gruut_ipa import Phonemes
import sys, os, json
import getopt

def save_info(data, output):
    json_data = ""
    with open(output, 'w', encoding='utf8') as outfile:
        json_data = json.dump(obj=data, fp=outfile, indent=4, ensure_ascii=False)
    return json_data

def parse_options(argv):
    verbose = False
    input = ""
    output = ""
    try:
        opts, args = getopt.getopt(argv,"hvi:o:",["input="])
    except getopt.GetoptError:
        print('-v <verbose> -i {text} <input> -o {filename.json} <output>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('-v <verbose> -i {text} <input> -o {filename} <output>')
            sys.exit()
        elif opt in ("-i", "--input"):
            input = arg
        elif opt in ("-o", "--output"):
            output = arg
        elif opt in ("-v", "--verbose"):
            verbose = True
    return verbose, input, output

def main(argv):
    filename = ""
    info = None
    verbose, input, output = parse_options(argv)
    if output != "":
        filename = output
        info = []
    pron_str = ipa.convert(input)
    if verbose:
        print("input:{input} ipa: {pron_str}".format(input=input, pron_str=pron_str))
    lang_phonemes = Phonemes.from_language("en-us")
    pron_phonemes = lang_phonemes.split(pron_str, keep_stress=True)
    for ipa_str in pron_phonemes:     
        phone = Phone.from_string(str(ipa_str)) 
        data = {}
        data["text"] = phone.text
        data["letters"] = phone.letters
        data["is_nasal"] = phone.is_nasal
        data["is_long"] = phone.is_long
        data["is_vowel"] = phone.is_vowel
        if phone.is_vowel:
            data["vowel"] = {}
            data["vowel"]["height"] = phone.vowel.height
            data["vowel"]["placement"] = phone.vowel.placement
        info.append(data)
        try:
            if verbose:
                print("text = {text}".format(text=phone.text))
                print("letters = {letters}".format(letters=phone.letters))
                print("diacritics[0] = {diacritics}".format(diacritics=phone.diacritics[0]))
                print("suprasegmentals = {suprasegmentals}".format(suprasegmentals=phone.suprasegmentals))
                print("stress = {stress}".format(stress=phone.stress))
                print("is_nasal = {is_nasal}".format(is_nasal=phone.is_nasal))
                print("is_long = {is_long}".format(is_long=phone.is_long))
                print("is_vowel = {is_vowel}".format(is_vowel=phone.is_vowel))
                if phone.is_vowel:
                    print("vowel.height = {height}".format(height=phone.vowel.height))
                    print("vowel.placement = {placement}".format(placement=phone.vowel.placement))
        except:
            pass
    if filename != "":
        data = save_info(info, filename)
        if verbose:
            print("file: {name}".format(name=filename))
            with open(filename, 'r', encoding='utf8') as outfile:
                print(outfile.read())
    
    #phoneme_strs = [p.text for p in pron_phonemes]
if __name__ == "__main__":
   main(sys.argv[1:])