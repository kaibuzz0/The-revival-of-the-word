#!/usr/bin/env python3
"""
Old Georgian Lexicon Builder
Builds an Old Georgian-English dictionary for ancient Georgian texts
"""
import json
import re
import sys
from pathlib import Path
from collections import defaultdict

# Core Old Georgian vocabulary
# Ancient Georgian (Kartvelian) language - 5th-11th centuries CE

OLD_GEORGIAN_CORE_VOCABULARY = {
    # Pronouns and Articles
    "მე": {"def": "I, me", "pos": "pronoun", "translit": "me", "root": "me"},
    "შენ": {"def": "you (singular)", "pos": "pronoun", "translit": "shen", "root": "shen"},
    "ის": {"def": "he, she, it, that", "pos": "pronoun/demonstrative", "translit": "is", "root": "is"},
    "ჩვენ": {"def": "we", "pos": "pronoun", "translit": "chven", "root": "chven"},
    "თქვენ": {"def": "you (plural)", "pos": "pronoun", "translit": "tkven", "root": "tkven"},
    "ისინი": {"def": "they", "pos": "pronoun", "translit": "isini", "root": "is"},
    "ეს": {"def": "this", "pos": "demonstrative", "translit": "es", "root": "es"},
    "იგი": {"def": "that one, he, she", "pos": "demonstrative", "translit": "igi", "root": "igi"},
    "რა": {"def": "what, which", "pos": "interrogative", "translit": "ra", "root": "ra"},
    "ვინ": {"def": "who", "pos": "interrogative", "translit": "vin", "root": "vin"},
    "რომელი": {"def": "which", "pos": "relative", "translit": "romeli", "root": "rom"},
    
    # Divine Names
    "ღმერთი": {"def": "God", "pos": "noun", "translit": "ghmerti", "root": "ghmer", "note": "The standard word for God in Georgian"},
    "უფალი": {"def": "Lord, Master", "pos": "noun", "translit": "upali", "root": "upal", "note": "Used for 'Lord' in Georgian Bible"},
    "იესუ": {"def": "Jesus", "pos": "proper noun", "translit": "iesu", "root": "iesu"},
    "ქრისტე": {"def": "Christ", "pos": "proper noun", "translit": "kriste", "root": "krist"},
    "მაცხოვარი": {"def": "Savior, Redeemer", "pos": "noun", "translit": "matskhovari", "root": "matskhov"},
    "სული წმიდა": {"def": "Holy Spirit", "pos": "proper noun", "translit": "suli tsmida", "root": "sul; tsmid"},
    "მამა": {"def": "father", "pos": "noun", "translit": "mama", "root": "mam"},
    "ძე": {"def": "son", "pos": "noun", "translit": "dze", "root": "dz"},
    "მარიამი": {"def": "Mary", "pos": "proper noun", "translit": "mariami", "root": "mariam"},
    "პეტრე": {"def": "Peter", "pos": "proper noun", "translit": "p'et're", "root": "p'etr"},
    "პავლე": {"def": "Paul", "pos": "proper noun", "translit": "p'avle", "root": "p'avl"},
    "იოვანე": {"def": "John", "pos": "proper noun", "translit": "iovane", "root": "iovan"},
    "მეფე": {"def": "king", "pos": "noun", "translit": "mephe", "root": "meph"},
    "სამეფო": {"def": "kingdom", "pos": "noun", "translit": "samepho", "root": "meph"},
    "ანგელოზი": {"def": "angel", "pos": "noun", "translit": "angelozi", "root": "angeloz"},
    "ზეცა": {"def": "heaven, sky", "pos": "noun", "translit": "zetsa", "root": "zets"},
    "ცა": {"def": "sky, heaven", "pos": "noun", "translit": "tsa", "root": "ts"},
    
    # Common Nouns
    "კაცი": {"def": "man, human", "pos": "noun", "translit": "katsi", "root": "kats"},
    "ქალი": {"def": "woman, wife", "pos": "noun", "translit": "kali", "root": "kal"},
    "ბავშვი": {"def": "child", "pos": "noun", "translit": "bavshvi", "root": "bavshv"},
    "ყრმა": {"def": "infant, baby", "pos": "noun", "translit": "q'rma", "root": "q'rm"},
    "სახლი": {"def": "house, home", "pos": "noun", "translit": "sakhli", "root": "sakhl"},
    "გული": {"def": "heart", "pos": "noun", "translit": "guli", "root": "gul"},
    "სული": {"def": "soul, spirit", "pos": "noun", "translit": "suli", "root": "sul"},
    "კერძო": {"def": "body", "pos": "noun", "translit": "kerdzo", "root": "kerdz"},
    "ჰიერს": {"def": "body", "pos": "noun", "translit": "hiers", "root": "hier"},
    "სისხლი": {"def": "blood", "pos": "noun", "translit": "siskhli", "root": "siskhl"},
    "ხორცი": {"def": "flesh, meat", "pos": "noun", "translit": "khortsi", "root": "khorts"},
    "თვალი": {"def": "eye", "pos": "noun", "translit": "tvali", "root": "tval"},
    "ყური": {"def": "ear", "pos": "noun", "translit": "q'uri", "root": "q'ur"},
    "ხელი": {"def": "hand, arm", "pos": "noun", "translit": "kheli", "root": "khel"},
    "თავი": {"def": "head", "pos": "noun", "translit": "tavi", "root": "tav"},
    "პირი": {"def": "mouth, face", "pos": "noun", "translit": "p'iri", "root": "p'ir"},
    "წყალი": {"def": "water", "pos": "noun", "translit": "tsqali", "root": "tsqal"},
    "ცეცხლი": {"def": "fire", "pos": "noun", "translit": "tsetskhli", "root": "tsetskhl"},
    "მიწა": {"def": "earth, land, ground", "pos": "noun", "translit": "mitsa", "root": "mits"},
    "მზე": {"def": "sun", "pos": "noun", "translit": "mze", "root": "mz"},
    "მთვარე": {"def": "moon", "pos": "noun", "translit": "mtvare", "root": "mtvar"},
    "შუქი": {"def": "light", "pos": "noun", "translit": "shuki", "root": "shuk"},
    "სიბნელე": {"def": "darkness", "pos": "noun", "translit": "sibnele", "root": "sibnel"},
    "ხე": {"def": "tree, wood", "pos": "noun", "translit": "khe", "root": "kh"},
    "გზა": {"def": "road, way, path", "pos": "noun", "translit": "gza", "root": "gz"},
    "დღე": {"def": "day", "pos": "noun", "translit": "dghe", "root": "dgh"},
    "ღამე": {"def": "night", "pos": "noun", "translit": "ghame", "root": "gham"},
    
    # Verbs
    "თქვა": {"def": "to say, speak", "pos": "verb", "translit": "tkva", "root": "tkv"},
    "ყოფა": {"def": "to be, exist", "pos": "verb", "translit": "q'opa", "root": "q'op"},
    "ყოფილ": {"def": "to have been", "pos": "verb", "translit": "q'opil", "root": "q'op"},
    "ჰყავს": {"def": "to have", "pos": "verb", "translit": "hq'avs", "root": "hq'av"},
    "ჰქმნა": {"def": "to do, make", "pos": "verb", "translit": "hq'mna", "root": "hq'mn"},
    "იცის": {"def": "to know", "pos": "verb", "translit": "itsis", "root": "its"},
    "ნახავს": {"def": "to see", "pos": "verb", "translit": "nakhavs", "root": "nakh"},
    "ესმის": {"def": "to hear", "pos": "verb", "translit": "esmis", "root": "esm"},
    "მისცა": {"def": "to give", "pos": "verb", "translit": "mitsa", "root": "mits"},
    "მიიღო": {"def": "to take, receive", "pos": "verb", "translit": "miigho", "root": "miigh"},
    "მოვიდა": {"def": "to come", "pos": "verb", "translit": "movida", "root": "movid"},
    "წავიდა": {"def": "to go", "pos": "verb", "translit": "tsavida", "root": "tsavid"},
    "დადგა": {"def": "to stand, rise", "pos": "verb", "translit": "dadga", "root": "dadg"},
    "აღდგა": {"def": "to rise up, be resurrected", "pos": "verb", "translit": "aghadga", "root": "aghadg"},
    "ცხონდა": {"def": "to live", "pos": "verb", "translit": "tshchonda", "root": "tshchond"},
    "მოკვდა": {"def": "to die", "pos": "verb", "translit": "moq'vda", "root": "moq'vd"},
    "მოჰკლა": {"def": "to kill", "pos": "verb", "translit": "mohqkla", "root": "mohqkl"},
    "წერა": {"def": "to write", "pos": "verb", "translit": "ts'era", "root": "ts'er"},
    "დაწერა": {"def": "to write", "pos": "verb", "translit": "dats'era", "root": "dats'er"},
    "დაუძახა": {"def": "to call", "pos": "verb", "translit": "daudzakha", "root": "daudzakh"},
    "გახსნა": {"def": "to open", "pos": "verb", "translit": "gakhna", "root": "gakhn"},
    "დაკეტა": {"def": "to close, shut", "pos": "verb", "translit": "daketa", "root": "daket"},
    "დაწვა": {"def": "to lie down, sleep", "pos": "verb", "translit": "datsva", "root": "datsv"},
    "აშენა": {"def": "to build", "pos": "verb", "translit": "ashena", "root": "ashen"},
    "მოსვა": {"def": "to drink", "pos": "verb", "translit": "mosva", "root": "mosv"},
    "ჭამა": {"def": "to eat", "pos": "verb", "translit": "ch'ama", "root": "ch'am"},
    "შეერია": {"def": "to put on, wear", "pos": "verb", "translit": "sheria", "root": "sher"},
    "შეაბა": {"def": "to bind, fasten", "pos": "verb", "translit": "sheaba", "root": "sheab"},
    "გაგზავნა": {"def": "to send", "pos": "verb", "translit": "gagzavna", "root": "gagzavn"},
    "ჰმართ": {"def": "to love, like", "pos": "verb", "translit": "hmart", "root": "hmart"},
    "ჰმადლობს": {"def": "to love, be grateful", "pos": "verb", "translit": "hmadlobs", "root": "hmadlob"},
    
    # Prepositions and Postpositions
    "ში": {"def": "in, into", "pos": "postposition", "translit": "shi", "root": "sh"},
    "ზე": {"def": "on, upon, over", "pos": "postposition", "translit": "ze", "root": "z"},
    "თვის": {"def": "for", "pos": "postposition", "translit": "tvis", "root": "tvis"},
    "გამო": {"def": "because of, for", "pos": "postposition", "translit": "gamo", "root": "gam"},
    "კენ": {"def": "toward", "pos": "postposition", "translit": "k'en", "root": "k'en"},
    "გან": {"def": "from", "pos": "postposition", "translit": "gan", "root": "gan"},
    "მდე": {"def": "up to, until", "pos": "postposition", "translit": "mde", "root": "mde"},
    "თან": {"def": "with", "pos": "postposition", "translit": "tan", "root": "tan"},
    "შორის": {"def": "between, among", "pos": "postposition", "translit": "shoris", "root": "shor"},
    "უკენ": {"def": "behind, after", "pos": "postposition", "translit": "uk'en", "root": "uk'en"},
    "წინ": {"def": "before, in front of", "pos": "postposition", "translit": "tsin", "root": "tsin"},
    
    # Conjunctions
    "და": {"def": "and", "pos": "conjunction", "translit": "da", "root": "d"},
    "მაგრამ": {"def": "but, however", "pos": "conjunction", "translit": "magaram", "root": "magar"},
    "ან": {"def": "or", "pos": "conjunction", "translit": "an", "root": "an"},
    "თუ": {"def": "if", "pos": "conjunction", "translit": "tu", "root": "tu"},
    "რომ": {"def": "that, because", "pos": "conjunction", "translit": "rom", "root": "rom"},
    "რადგან": {"def": "because, for", "pos": "conjunction", "translit": "radgan", "root": "radgan"},
    "ვინაიდან": {"def": "since, because", "pos": "conjunction", "translit": "vinaidan", "root": "vinaid"},
    "ანუ": {"def": "that is, namely", "pos": "conjunction", "translit": "anu", "root": "anu"},
    
    # Negatives
    "არ": {"def": "not", "pos": "negative particle", "translit": "ar", "root": "ar"},
    "არა": {"def": "no, not", "pos": "negative", "translit": "ara", "root": "ar"},
    
    # Adjectives
    "კეთილი": {"def": "good, kind", "pos": "adjective", "translit": "ketili", "root": "ketil"},
    "ცუდი": {"def": "bad, evil", "pos": "adjective", "translit": "tsudi", "root": "tsud"},
    "დიდი": {"def": "great, big, large", "pos": "adjective", "translit": "didi", "root": "did"},
    "პატარა": {"def": "small, little", "pos": "adjective", "translit": "p'at'ara", "root": "p'at'ar"},
    "წმიდა": {"def": "holy, sacred", "pos": "adjective", "translit": "tsmida", "root": "tsmid"},
    "მართალი": {"def": "just, righteous", "pos": "adjective", "translit": "martali", "root": "martal"},
    "ჭეშმარიტი": {"def": "true, faithful", "pos": "adjective", "translit": "ch'eshmariti", "root": "ch'eshmarit"},
    "ახალი": {"def": "new", "pos": "adjective", "translit": "akhali", "root": "akhal"},
    "ძველი": {"def": "old, ancient", "pos": "adjective", "translit": "dzveli", "root": "dzvel"},
    "მაღალი": {"def": "high, tall", "pos": "adjective", "translit": "maghali", "root": "maghal"},
    "დაბალი": {"def": "low", "pos": "adjective", "translit": "dabali", "root": "dabal"},
    "ძლიერი": {"def": "strong, mighty", "pos": "adjective", "translit": "dzlieri", "root": "dzlier"},
    "რბილი": {"def": "soft, tender", "pos": "adjective", "translit": "rbili", "root": "rbil"},
    "უძველესი": {"def": "oldest, most ancient", "pos": "adjective", "translit": "udzvelesi", "root": "udzveles"},
    "პირველი": {"def": "first", "pos": "adjective/numeral", "translit": "p'irveli", "root": "p'irvel"},
    "ბოლო": {"def": "last", "pos": "adjective", "translit": "bolo", "root": "bol"},
    "უკანასკნელი": {"def": "last, final", "pos": "adjective", "translit": "ukanaskneli", "root": "ukanasknel"},
    
    # Numbers
    "ერთი": {"def": "one", "pos": "numeral", "translit": "erti", "root": "ert"},
    "ორი": {"def": "two", "pos": "numeral", "translit": "ori", "root": "or"},
    "სამი": {"def": "three", "pos": "numeral", "translit": "sami", "root": "sam"},
    "ოთხი": {"def": "four", "pos": "numeral", "translit": "otkhi", "root": "otkh"},
    "ხუთი": {"def": "five", "pos": "numeral", "translit": "khuti", "root": "khut"},
    "ათი": {"def": "ten", "pos": "numeral", "translit": "ati", "root": "at"},
    "ასი": {"def": "hundred", "pos": "numeral", "translit": "asi", "root": "as"},
    "ათასი": {"def": "thousand", "pos": "numeral", "translit": "atasi", "root": "atas"},
    
    # Theological/Ecclesiastical Terms
    "ეკლესია": {"def": "church", "pos": "noun", "translit": "ek'lesia", "root": "ek'les"},
    "საიდუმლო": {"def": "mystery, sacrament", "pos": "noun", "translit": "saidumlo", "root": "saiduml"},
    "წირვა": {"def": "liturgy, service", "pos": "noun", "translit": "ts'irva", "root": "ts'irv"},
    "სულთმოფენობა": {"def": "Pentecost", "pos": "noun", "translit": "sultmophenoba", "root": "sultmophen"},
    "განსაკუთრებული": {"def": "holy, separate", "pos": "adjective", "translit": "gansak'utrebul", "root": "gansak'utreb"},
    "ღვთისმოსავი": {"def": "godly, pious", "pos": "adjective", "translit": "ghvtismosavi", "root": "ghvtismosav"},
    "მორწმუნე": {"def": "believer", "pos": "noun", "translit": "morts'mune", "root": "morts'mun"},
    "სარწმუნოება": {"def": "faith, religion", "pos": "noun", "translit": "sarts'munoeba", "root": "sarts'muno"},
    "სასოება": {"def": "hope", "pos": "noun", "translit": "sasoeba", "root": "saso"},
    "ჰსურათი": {"def": "image, icon", "pos": "noun", "translit": "hsurati", "root": "hsurat"},
    "სიყვარული": {"def": "love", "pos": "noun", "translit": "siq'varuli", "root": "siq'varul"},
    "მოყვარული": {"def": "lover, friend", "pos": "noun", "translit": "moq'aruli", "root": "moq'arul"},
    "ჭეშმარიტება": {"def": "truth", "pos": "noun", "translit": "ch'eshmarit'eba", "root": "ch'eshmarit'"},
    "სამართალი": {"def": "justice, righteousness", "pos": "noun", "translit": "samartali", "root": "samartal"},
    "წყალობა": {"def": "grace, mercy", "pos": "noun", "translit": "tsqaloba", "root": "tsqalob"},
    "ცოდვა": {"def": "sin", "pos": "noun", "translit": "tsodva", "root": "tsodv"},
    "ცოდვილი": {"def": "sinner", "pos": "noun/adjective", "translit": "tsodvili", "root": "tsodvil"},
    "მონანიება": {"def": "repentance", "pos": "noun", "translit": "monanieba", "root": "monan"},
    "შენდობა": {"def": "forgiveness", "pos": "noun", "translit": "shendoba", "root": "shendob"},
    "შეწყალება": {"def": "mercy, compassion", "pos": "noun", "translit": "shetsoyaleba", "root": "shetsoyaleb"},
    "დიდება": {"def": "glory, praise", "pos": "noun", "translit": "dideba", "root": "dideb"},
    "ქება": {"def": "praise", "pos": "noun", "translit": "k'eba", "root": "k'eb"},
    "საქმე": {"def": "work, deed", "pos": "noun", "translit": "sak'me", "root": "sak'm"},
    "რწმენა": {"def": "belief, faith", "pos": "noun", "translit": "rts'mena", "root": "rts'men"},
    "ქადაგება": {"def": "preaching, sermon", "pos": "noun", "translit": "k'adageba", "root": "k'adageb"},
    "სწავლა": {"def": "teaching, doctrine", "pos": "noun", "translit": "sts'avla", "root": "sts'avl"},
    "განბანა": {"def": "baptism", "pos": "noun", "translit": "ganbana", "root": "ganban"},
    "ჯვარი": {"def": "cross", "pos": "noun", "translit": "jvri", "root": "jvr"},
    "კვდირობა": {"def": "death", "pos": "noun", "translit": "k'vdiroba", "root": "k'vdirob"},
    "კვდირობისგან": {"def": "from death", "pos": "noun", "translit": "k'vdirobigsa", "root": "k'vdirobsgan"},
    "განკვდომა": {"def": "resurrection", "pos": "noun", "translit": "gank'vdoma", "root": "gank'vdom"},
    "სიცოცხლე": {"def": "life", "pos": "noun", "translit": "sists'k'hle", "root": "sists'k'hl"},
    "წმიდა წერილი": {"def": "Holy Scripture", "pos": "noun phrase", "translit": "tsmida ts'erili", "root": "tsmid; ts'eril"},
    "წმიდა": {"def": "holy one, saint", "pos": "noun/adjective", "translit": "tsmida", "root": "tsmid"},
    "მოციქული": {"def": "apostle", "pos": "noun", "translit": "motsik'uli", "root": "motsik'ul"},
    "სახარება": {"def": "gospel", "pos": "noun", "translit": "sakhareba", "root": "sakhareb"},
    "ძველი აღთქმა": {"def": "Old Testament", "pos": "noun phrase", "translit": "dzveli aghat'k'ma", "root": "dzvel; aghat'k'm"},
    "ახალი აღთქმა": {"def": "New Testament", "pos": "noun phrase", "translit": "akhali aghat'k'ma", "root": "akhal; aghat'k'm"},
    "წინასწარმეტყველი": {"def": "prophet", "pos": "noun", "translit": "ts'inasatsarmet'yvleli", "root": "ts'inasatsarmet'yvlel"},
    "მღვდელმთავარი": {"def": "high priest", "pos": "noun", "translit": "mghvdelmtavari", "root": "mghvdelmtavar"},
    "მღვდელი": {"def": "priest", "pos": "noun", "translit": "mghvdeli", "root": "mghvdel"},
    "მთავარეპისკოპოსი": {"def": "archbishop, catholicos", "pos": "noun", "translit": "mtavarepiskoposi", "root": "mtavarepiskopos"},
    "ეპისკოპოსი": {"def": "bishop", "pos": "noun", "translit": "episkoposi", "root": "episkopos"},
    "მონაზონი": {"def": "monk", "pos": "noun", "translit": "monazoni", "root": "monazon"},
    "ნუნი": {"def": "nun", "pos": "noun", "translit": "nuni", "root": "nun"},
    "სავანე": {"def": "monastery", "pos": "noun", "translit": "savane", "root": "savan"},
    "ტაძარი": {"def": "temple, church building", "pos": "noun", "translit": "tadzari", "root": "tadzar"},
    "სამსხვერპლო": {"def": "altar", "pos": "noun", "translit": "samsakhverplo", "root": "samsakhverpl"},
    "პური": {"def": "bread", "pos": "noun", "translit": "p'uri", "root": "p'ur"},
    "ღვინო": {"def": "wine", "pos": "noun", "translit": "ghvino", "root": "ghvin"},
    "ზეთი": {"def": "oil", "pos": "noun", "translit": "zeti", "root": "zet"},
    "სანთელი": {"def": "candle, lamp", "pos": "noun", "translit": "santeli", "root": "santel"},
    "საკმი": {"def": "incense", "pos": "noun", "translit": "sakmi", "root": "sakm"},
    "სამოთხე": {"def": "paradise, heaven", "pos": "noun", "translit": "samotkhe", "root": "samotkh"},
    "ნაქსოვი": {"def": "hell", "pos": "noun", "translit": "naksovi", "root": "naksov"},
    "ეშმაკი": {"def": "devil, demon", "pos": "noun", "translit": "eshmaki", "root": "eshmak"},
    "ბოროტი": {"def": "evil one, devil", "pos": "noun/adjective", "translit": "boroti", "root": "borot"},
    "ლოცვა": {"def": "prayer", "pos": "noun", "translit": "lotsva", "root": "lotsv"},
    "ჰმადლობა": {"def": "thanksgiving", "pos": "noun", "translit": "hmadloba", "root": "hmadlob"},
    "ვედრება": {"def": "supplication", "pos": "noun", "translit": "vedreba", "root": "vedreb"},
    "შებრძნება": {"def": "humility", "pos": "noun", "translit": "shebrdzneba", "root": "shebrdzneb"},
    "სიმდაბლე": {"def": "humility", "pos": "noun", "translit": "simdable", "root": "simdabl"},
    "სიწმინდე": {"def": "holiness", "pos": "noun", "translit": "sits'minde", "root": "sits'mind"},
    "სიწყალური": {"def": "mercy, compassion", "pos": "noun", "translit": "sits'qaluri", "root": "sits'qalur"},
    "სიმართლე": {"def": "righteousness, justice", "pos": "noun", "translit": "simartle", "root": "simartl"},
    "სათნოება": {"def": "virtue, goodness", "pos": "noun", "translit": "sat'noeba", "root": "sat'noeb"},
    "ყოველგავალი": {"def": "almighty", "pos": "adjective", "translit": "q'ovelgavali", "root": "q'ovelgaval"},
    "ყოვლადწმიდა": {"def": "all-holy", "pos": "adjective", "translit": "q'oveladtsmida", "root": "q'oveladtsmid"},
    "სამება": {"def": "Trinity", "pos": "noun", "translit": "sameba", "root": "sameb"},
    "მამათმთავარი": {"def": "God the Father", "pos": "noun", "translit": "mamatmtavari", "root": "mamatmtavar"},
}

# Extended vocabulary
OLD_GEORGIAN_EXTENDED_VOCABULARY = {
    # More body parts
    "ცხვირი": {"def": "nose", "pos": "noun", "translit": "tskhviri", "root": "tskhvir"},
    "ყელი": {"def": "throat, neck", "pos": "noun", "translit": "q'eli", "root": "q'el"},
    "ფრჩხილი": {"def": "nail, claw", "pos": "noun", "translit": "p'rchkhili", "root": "p'rchkhil"},
    "ტუჩი": {"def": "lip", "pos": "noun", "translit": "tuchi", "root": "tuch"},
    "ყრუ": {"def": "deaf", "pos": "adjective", "translit": "q'ru", "root": "q'r"},
    "კბილი": {"def": "tooth", "pos": "noun", "translit": "k'bili", "root": "k'bil"},
    "ნაკვრცი": {"def": "lip", "pos": "noun", "translit": "nak'vrtsi", "root": "nak'vrts"},
    "გუგა": {"def": "eyeball, pupil", "pos": "noun", "translit": "guga", "root": "gug"},
    "წარბი": {"def": "eyebrow", "pos": "noun", "translit": "ts'rbi", "root": "ts'rab"},
    "ყურძენი": {"def": "ankle, wrist", "pos": "noun", "translit": "q'urdzeni", "root": "q'urdzen"},
    "გულმკერდი": {"def": "chest", "pos": "noun", "translit": "gulmk'erdi", "root": "gulmk'erd"},
    "მუცელი": {"def": "stomach, belly", "pos": "noun", "translit": "mutseli", "root": "mutsel"},
    "ხერხემალი": {"def": "spine, back", "pos": "noun", "translit": "kherkhemali", "root": "kherkhemal"},
    "ზურგი": {"def": "back", "pos": "noun", "translit": "zurgi", "root": "zurg"},
    "ბეჭი": {"def": "shoulder", "pos": "noun", "translit": "bechi", "root": "bech"},
    "თმა": {"def": "hair", "pos": "noun", "translit": "tma", "root": "tm"},
    "წვერი": {"def": "beard", "pos": "noun", "translit": "ts'veri", "root": "ts'ver"},
    "ულვაში": {"def": "mustache", "pos": "noun", "translit": "ulvashi", "root": "ulvash"},
    
    # More nature
    "მთა": {"def": "mountain", "pos": "noun", "translit": "mta", "root": "mt"},
    "ბოგირი": {"def": "hill", "pos": "noun", "translit": "bogiri", "root": "bogir"},
    "ჭალა": {"def": "valley, ravine", "pos": "noun", "translit": "ch'ala", "root": "ch'al"},
    "ზღვა": {"def": "sea", "pos": "noun", "translit": "zgva", "root": "zgv"},
    "ტბა": {"def": "lake", "pos": "noun", "translit": "tba", "root": "tb"},
    "ნაკადი": {"def": "stream", "pos": "noun", "translit": "nakadi", "root": "nakad"},
    "აკვანი": {"def": "pool", "pos": "noun", "translit": "ak'vani", "root": "ak'van"},
    "ჭა": {"def": "well", "pos": "noun", "translit": "ch'a", "root": "ch'"},
    "ქვაბი": {"def": "cave", "pos": "noun", "translit": "k'vabi", "root": "k'vab"},
    "კლდე": {"def": "rock, cliff", "pos": "noun", "translit": "k'le", "root": "k'ld"},
    "ქვა": {"def": "stone", "pos": "noun", "translit": "k'va", "root": "k'v"},
    "კარი": {"def": "cave", "pos": "noun", "translit": "k'ari", "root": "k'ar"},
    "თხრობა": {"def": "digging", "pos": "noun", "translit": "takhroba", "root": "takhrob"},
    "დაბლობი": {"def": "plain, lowland", "pos": "noun", "translit": "dablobi", "root": "dablob"},
    "ველი": {"def": "plain, field", "pos": "noun", "translit": "veli", "root": "vel"},
    "ნავსი": {"def": "meadow, pasture", "pos": "noun", "translit": "navsi", "root": "navs"},
    "ტყე": {"def": "forest, woods", "pos": "noun", "translit": "tqe", "root": "tq"},
    "ჭაობი": {"def": "swamp, marsh", "pos": "noun", "translit": "ch'aobi", "root": "ch'aob"},
    "ნახირი": {"def": "frost", "pos": "noun", "translit": "nakhri", "root": "nakhr"},
    "ყინვა": {"def": "cold, frost", "pos": "noun", "translit": "q'invai", "root": "q'inv"},
    "თოვლი": {"def": "snow", "pos": "noun", "translit": "tovli", "root": "tovl"},
    "წვიმა": {"def": "rain", "pos": "noun", "translit": "ts'vima", "root": "ts'vim"},
    "ქარი": {"def": "wind", "pos": "noun", "translit": "k'ari", "root": "k'ar"},
    "ჭექა": {"def": "thunder", "pos": "noun", "translit": "ch'eka", "root": "ch'ek"},
    "ელვა": {"def": "lightning", "pos": "noun", "translit": "elva", "root": "elv"},
    "ბუგრი": {"def": "mist, fog", "pos": "noun", "translit": "bugri", "root": "bugr"},
    "ნისლი": {"def": "mist, vapor", "pos": "noun", "translit": "nisli", "root": "nisl"},
    "ნიავი": {"def": "breeze", "pos": "noun", "translit": "niavi", "root": "niav"},
    "გვალვა": {"def": "drought", "pos": "noun", "translit": "gvalva", "root": "gvalv"},
    
    # More abstract
    "გონება": {"def": "mind, intellect", "pos": "noun", "translit": "goneba", "root": "goneb"},
    "სულიწრფე": {"def": "soul, spirit", "pos": "noun", "translit": "sulits'rp'e", "root": "sulits'rp'"},
    "გრძნობა": {"def": "feeling, sense", "pos": "noun", "translit": "grdznobebi", "root": "grdznob"},
    "სურვილი": {"def": "desire, will", "pos": "noun", "translit": "survili", "root": "survil"},
    "აზრი": {"def": "thought, idea", "pos": "noun", "translit": "azri", "root": "azr"},
    "განზრახვა": {"def": "intention, purpose", "pos": "noun", "translit": "ganzirakhva", "root": "ganzirakhv"},
    "მიზანი": {"def": "goal, aim", "pos": "noun", "translit": "mizani", "root": "mizan"},
    "მიზეზი": {"def": "cause, reason", "pos": "noun", "translit": "mizezi", "root": "mizez"},
    "სახელი": {"def": "name", "pos": "noun", "translit": "sakheli", "root": "sakhel"},
    "საგანი": {"def": "thing, matter", "pos": "noun", "translit": "sagani", "root": "sagan"},
    "ქონება": {"def": "possession, wealth", "pos": "noun", "translit": "k'oneba", "root": "k'oneb"},
    "ყოფა": {"def": "existence, being", "pos": "noun", "translit": "q'opa", "root": "q'op"},
    "ბუნება": {"def": "nature", "pos": "noun", "translit": "buneba", "root": "buneb"},
    "წესი": {"def": "law, rule", "pos": "noun", "translit": "ts'esi", "root": "ts'es"},
    "გზისწესი": {"def": "way, manner", "pos": "noun", "translit": "gzists'esi", "root": "gzists'es"},
    "საქმიანობა": {"def": "activity", "pos": "noun", "translit": "sak'mianoba", "root": "sak'mianob"},
    "შრომა": {"def": "labor, work", "pos": "noun", "translit": "shroma", "root": "shrom"},
    "ყოფნა": {"def": "presence, existence", "pos": "noun", "translit": "q'opna", "root": "q'opn"},
    "შემთხვევა": {"def": "event, circumstance", "pos": "noun", "translit": "shenmtkhveva", "root": "shenmtkhvev"},
    
    # Animals
    "ცხოველი": {"def": "animal, living creature", "pos": "noun", "translit": "tshovali", "root": "tshoval"},
    "ფრინველი": {"def": "bird", "pos": "noun", "translit": "p'irnveli", "root": "p'irnvel"},
    "თევზი": {"def": "fish", "pos": "noun", "translit": "tevzi", "root": "tevz"},
    "გველი": {"def": "snake, serpent", "pos": "noun", "translit": "gveli", "root": "gvel"},
    "კურდღელი": {"def": "rabbit, hare", "pos": "noun", "translit": "k'urdghli", "root": "k'urdghl"},
    "თაგუნია": {"def": "fox", "pos": "noun", "translit": "tagunia", "root": "tagun"},
    "მგელი": {"def": "wolf", "pos": "noun", "translit": "mgeli", "root": "mgel"},
    "დათვი": {"def": "bear", "pos": "noun", "translit": "dat'vi", "root": "dat'v"},
    "კატუ": {"def": "cat", "pos": "noun", "translit": "k'at'u", "root": "k'at'"},
    "ძაღლი": {"def": "dog", "pos": "noun", "translit": "dzagli", "root": "dzagl"},
    "ცხენი": {"def": "horse", "pos": "noun", "translit": "tskeni", "root": "tsken"},
    "ხარი": {"def": "ox, bull", "pos": "noun", "translit": "khari", "root": "khar"},
    "ძროხა": {"def": "cow", "pos": "noun", "translit": "dzrokh", "root": "dzrokh"},
    "ცხვარი": {"def": "sheep", "pos": "noun", "translit": "tskhvari", "root": "tskhvar"},
    "თხა": {"def": "goat", "pos": "noun", "translit": "tkha", "root": "tkh"},
    "ღორი": {"def": "pig", "pos": "noun", "translit": "ghori", "root": "ghor"},
    "გარეული": {"def": "wild (animal)", "pos": "adjective", "translit": "gareuli", "root": "gareul"},
    "მთისა": {"def": "of the mountain", "pos": "adjective", "translit": "mtisa", "root": "mtis"},
    
    # Colors
    "თეთრი": {"def": "white", "pos": "adjective", "translit": "tet'ri", "root": "tet'r"},
    "შავი": {"def": "black", "pos": "adjective", "translit": "shavi", "root": "shav"},
    "წითელი": {"def": "red", "pos": "adjective", "translit": "ts'iteli", "root": "ts'itel"},
    "მწვანე": {"def": "green", "pos": "adjective", "translit": "mts'vane", "root": "mts'van"},
    "ლურჯი": {"def": "blue", "pos": "adjective", "translit": "lurji", "root": "lurj"},
    "ყვითელი": {"def": "yellow", "pos": "adjective", "translit": "q'viteli", "root": "q'vitel"},
    "ნარინჯისფერი": {"def": "orange", "pos": "adjective", "translit": "narinjisperi", "root": "narinjisper"},
    "იასამნისფერი": {"def": "violet, purple", "pos": "adjective", "translit": "iasamnisperi", "root": "iasamnisper"},
    "უფოსფერი": {"def": "brown", "pos": "adjective", "translit": "up'osperi", "root": "up'osper"},
    "რუხი": {"def": "gray", "pos": "adjective", "translit": "rukhi", "root": "rukh"},
    "ბადაგი": {"def": "spotted, speckled", "pos": "adjective", "translit": "badagi", "root": "badag"},
    
    # Materials
    "ოქრო": {"def": "gold", "pos": "noun", "translit": "ok'ro", "root": "ok'r"},
    "ვერცხლი": {"def": "silver", "pos": "noun", "translit": "vertskhli", "root": "vertskhl"},
    "სპილენძი": {"def": "copper, bronze", "pos": "noun", "translit": "sp'ilendzi", "root": "sp'ilendz"},
    "ტყვია": {"def": "lead", "pos": "noun", "translit": "tqviai", "root": "tqv"},
    "რკინა": {"def": "iron", "pos": "noun", "translit": "rk'ina", "root": "rk'in"},
    "თუჯი": {"def": "copper ore", "pos": "noun", "translit": "tuji", "root": "tuj"},
    "ბრინჯაო": {"def": "bronze", "pos": "noun", "translit": "brinjao", "root": "brinja"},
    "ხე": {"def": "wood", "pos": "noun", "translit": "khe", "root": "kh"},
    "ნაჭერი": {"def": "cloth, fabric", "pos": "noun", "translit": "nach'eri", "root": "nach'er"},
    "მატერია": {"def": "material, fabric", "pos": "noun", "translit": "mat'eria", "root": "mat'er"},
    "ტყავი": {"def": "leather, hide", "pos": "noun", "translit": "tqvavi", "root": "tqvav"},
    "მინა": {"def": "glass", "pos": "noun", "translit": "mina", "root": "min"},
    "თიხა": {"def": "clay", "pos": "noun", "translit": "tikha", "root": "tikh"},
    "ბალახი": {"def": "grass, hay", "pos": "noun", "translit": "balakhi", "root": "balakh"},
    "ჩალა": {"def": "straw", "pos": "noun", "translit": "ch'ala", "root": "ch'al"},
}

class OldGeorgianLexicon:
    """Old Georgian-English lexicon"""
    
    def __init__(self):
        self.entries = {}
        self.root_index = defaultdict(list)
        
    def build(self):
        """Build lexicon from vocabulary lists"""
        print("[*] Building Old Georgian lexicon...")
        
        # Combine vocabularies
        all_vocab = {**OLD_GEORGIAN_CORE_VOCABULARY, **OLD_GEORGIAN_EXTENDED_VOCABULARY}
        
        for word, data in all_vocab.items():
            entry = {
                "word": word,
                "definition": data["def"],
                "part_of_speech": data["pos"],
                "transliteration": data["translit"],
                "root": data["root"]
            }
            
            # Add optional note
            if "note" in data:
                entry["note"] = data["note"]
            
            self.entries[word] = entry
            
            # Index by root
            if data["root"]:
                for root_part in data["root"].split(";"):
                    self.root_index[root_part.strip()].append(word)
        
        print(f"    [+] Built {len(self.entries)} entries")
        
    def export_json(self, output_path: str):
        """Export to JSON"""
        print(f"[*] Exporting to {output_path}...")
        
        data = {
            "metadata": {
                "title": "Old Georgian Lexicon",
                "language": "Old Georgian (Kartvelian)",
                "script": "Georgian (Mkhedruli, Asomtavruli)",
                "period": "Old Georgian (5th-11th centuries CE)",
                "total_entries": len(self.entries),
                "format": "JSON",
                "notes": "Old Georgian is the language of the ancient Georgian Orthodox Church. Georgian is a Kartvelian (South Caucasian) language, unrelated to Indo-European or Semitic families."
            },
            "entries": self.entries,
            "root_index": dict(self.root_index)
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"    [+] Exported {len(self.entries)} entries")
    
    def export_markdown(self, output_path: str):
        """Export to Markdown"""
        print(f"[*] Exporting markdown to {output_path}...")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("# Old Georgian Lexicon\n\n")
            f.write("**Old Georgian-English Dictionary (Kartvelian)**\n\n")
            f.write(f"Total Entries: {len(self.entries)}\n\n")
            f.write("---\n\n")
            
            # Sort by Georgian word
            sorted_entries = sorted(self.entries.items(), key=lambda x: x[0])
            
            for word, entry in sorted_entries:
                f.write(f"## {word}\n\n")
                f.write(f"**Transliteration:** *{entry['transliteration']}*\n\n")
                f.write(f"**Part of Speech:** {entry['part_of_speech']}\n\n")
                f.write(f"**Definition:** {entry['definition']}\n\n")
                f.write(f"**Root:** {entry['root']}\n\n")
                if "note" in entry:
                    f.write(f"**Note:** {entry['note']}\n\n")
                f.write("---\n\n")
        
        print(f"    [+] Exported {len(self.entries)} entries")
    
    def export_websters_style(self, output_path: str):
        """Export in Webster's dictionary format"""
        print(f"[*] Exporting Webster's style to {output_path}...")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("=" * 70 + "\n")
            f.write("OLD GEORGIAN LEXICON\n")
            f.write("Old Georgian-English Dictionary (Kartvelian)\n")
            f.write("=" * 70 + "\n\n")
            
            f.write("About Old Georgian:\n")
            f.write("  - Kartvelian (South Caucasian) language family\n")
            f.write("  - UNRELATED to Indo-European or Semitic languages\n")
            f.write("  - Language of the ancient Georgian Orthodox Church\n")
            f.write("  - Three scripts: Asomtavruli (ancient), Nuskhuri (medieval), Mkhedruli (modern)\n")
            f.write("  - Unique alphabet with 33 letters\n")
            f.write("  - Agglutinative language (like Turkish, Finnish)\n\n")
            
            f.write("Pronunciation Guide:\n")
            f.write("  ა = a (father)        ი = i (machine)\n")
            f.write("  ე = e (pet)           ო = o (note)\n")
            f.write("  ი = i (machine)       უ = u (rule)\n")
            f.write("  გ = g (go)            ქ = k (king)\n")
            f.write("  დ = d (dog)           ლ = l (love)\n")
            f.write("  ვ = v (very)          მ = m (man)\n")
            f.write("  ზ = z (zebra)         ნ = n (no)\n")
            f.write("  თ = t (top)           პ = p' (emphatic p)\n")
            f.write("  ი = i (machine)       ჟ = zh (measure)\n")
            f.write("  კ = k' (emphatic k)   რ = r (rolled)\n")
            f.write("  ლ = l (love)          ს = s (see)\n")
            f.write("  მ = m (man)           ტ = t' (emphatic t)\n")
            f.write("  ნ = n (no)            უ = u (rule)\n")
            f.write("  ფ = p (spin)          ქ = k (king)\n")
            f.write("  ღ = gh (Arabic gh)     ყ = q (Semitic q)\n")
            f.write("  შ = sh (ship)         ჩ = ch (church)\n")
            f.write("  ც = ts (cats)         ძ = dz (adze)\n")
            f.write("  წ = ts' (emphatic)    ჭ = ch' (emphatic)\n")
            f.write("  ხ = kh (Scottish loch) ჯ = j (jump)\n")
            f.write("  ჰ = h (hat)           ჱ = ē (archaic)\n")
            f.write("  ჲ = y (yes)           ჳ = wī (archaic)\n")
            f.write("  ჴ = q' (archaic)      ჵ = hō (archaic)\n\n")
            
            f.write("-" * 70 + "\n\n")
            
            sorted_entries = sorted(self.entries.items(), key=lambda x: x[0])
            
            for word, entry in sorted_entries:
                f.write(f"\n{word}")
                if entry['transliteration']:
                    f.write(f"  ({entry['transliteration']})")
                
                f.write(f"  [{entry['part_of_speech']}]")
                f.write("\n")
                
                # Definition
                f.write(f"    {entry['definition']}\n")
                
                # Root
                if entry['root']:
                    f.write(f"    Root: {entry['root']}\n")
                
                # Note
                if "note" in entry:
                    f.write(f"    Note: {entry['note']}\n")
                
                f.write("\n")
        
        print(f"    [+] Exported {len(self.entries)} entries")
    
    def search(self, query: str) -> list:
        """Search the lexicon"""
        results = []
        query_lower = query.lower()
        
        for word, entry in self.entries.items():
            match = False
            
            if query_lower in word.lower():
                match = True
            elif query_lower in entry['definition'].lower():
                match = True
            elif query_lower in entry['transliteration'].lower():
                match = True
            elif query_lower in entry['root'].lower():
                match = True
            
            if match:
                results.append((word, entry))
        
        return results


def main():
    lexicon = OldGeorgianLexicon()
    
    # Build from vocabulary
    lexicon.build()
    
    # Create output directory
    out_dir = Path("/root/old_georgian_lexicon_output")
    out_dir.mkdir(parents=True, exist_ok=True)
    
    # Export all formats
    lexicon.export_json(out_dir / "old_georgian_lexicon.json")
    lexicon.export_markdown(out_dir / "old_georgian_lexicon.md")
    lexicon.export_websters_style(out_dir / "websters_old_georgian.txt")
    
    # Sample entries
    print("\n" + "=" * 70)
    print("SAMPLE ENTRIES")
    print("=" * 70 + "\n")
    
    sample_words = ['ღმერთი', 'უფალი', 'იესუ', 'ქრისტე', 'სული', 'სიყვარული']
    for word in sample_words:
        if word in lexicon.entries:
            e = lexicon.entries[word]
            print(f"{word} ({e['transliteration']})")
            print(f"  {e['definition']}")
            print(f"  [{e['part_of_speech']}] Root: {e['root']}\n")
    
    print("=" * 70)
    print("OLD GEORGIAN LEXICON COMPLETE")
    print("=" * 70)
    print(f"\nOutput files in {out_dir.absolute()}:")
    print(f"  - old_georgian_lexicon.json (full)")
    print(f"  - old_georgian_lexicon.md (human-readable)")
    print(f"  - websters_old_georgian.txt (Webster's style)")
    print(f"\nTo search: python search_old_georgian.py <word>")


if __name__ == "__main__":
    main()
