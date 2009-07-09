from Cheetah.Template import Template
from pyqcm import XmlQCM

templateDef = """
<?xml version="1.0" encoding="ISO-8859-1"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="fr"
lang="fr">
<head>
<meta http-equiv="Content-Type"
content="text/html; charset=ISO-8859-1" />
<title>Kataplop</title>
<link rel="stylesheet" type="text/css" href="/files/style.css" media="screen" />
</head>
<body>
<div id="main">

<div id="sidebar"><div id="titlebar"><a href="/pub/"><img src="/images/kataplop.png" alt="kataplop" /></a></div>
<div class="sbarentry">
<div class="sbtitle"><h2><a href="/pub/info">Informatique</a></h2></div>
<div class="sbaritem"><a href="/pub/info/linux_ipaq">Linux + iPaq</a></div>

<div class="sbaritem"><a href="/pub/info/hurd">Le Hurd</a></div>

<div class="sbaritem"><a href="/pub/info/projets">Projets</a></div>

<div class="sbaritem"><a href="/pub/info/bzr">Bazaar</a></div>

<div class="sbaritem"><a href="/pub/kataplop">Kataplop ?</a></div>

</div> <!-- sbarentry-->
<div class="sbarentry">
<div class="sbtitle"><h2><a href="/pub/loisirs">Loisirs</a></h2></div>
<div class="sbaritem"><a href="/pub/loisirs/parapente">Parapente</a></div>

<div class="sbaritem"><a href="/pub/loisirs/panoramas">Photos-Panoramas</a></div>

<div class="sbaritem"><a href="http://marc-photos.kataplop.net">Photos-Gallerie</a></div>

</div> <!-- sbarentry-->
<div class="sbarentry">
<div class="sbtitle"><h2><a href="/pub/contacts">Contacts</a></h2></div>
<div class="sbaritem"><a href="/pub/contacts/cv">CV</a></div>

</div> <!-- sbarentry-->
</div> <!-- sidebar -->

<div id="content"><h2>Kataplop</h2>

<p>
#for $question in $questions
<div class="question">
$question.qbody.encode('utf-8')
<ul>
#for item in $question.answers.items()
<li>
$item[0] ) $item[1][0].encode('utf-8')
</li>
#end for
</div>
#end for
</p>
</div> <!-- fin content -->
</div> <!-- main -->
</body>
</html>
"""

qcm = XmlQCM("../data/qcm_ffvl_2004.xml")
c_size = qcm.get_num_chapters()
qcm.select(number=30)

l=[]
for i in range(30):
    l += [qcm.getNext()]

t = Template(templateDef)

t.questions = l

print t

