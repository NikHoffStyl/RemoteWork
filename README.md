
![cms_higgsto4muons](https://user-images.githubusercontent.com/32751356/51404641-f1847e00-1b4b-11e9-88d4-eb94f7c02036.png)
# [Nikos - Four Top Production Repository](https://github.com/NikHoffStyl/RemoteWork)
Repository for Working in the Single Lepton tttt decay channel. 

## Combining High-Level-Trigger (HLT) :high_brightness:
### Datasets
Monte Carlo Datasets Studied in CMSSW_9_4_X, chosen according to the  [Particle Performance Dataset (PPD) RunII Analysis
Guideline](https://twiki.cern.ch/twiki/bin/viewauth/CMS/PdmVAnalysisSummaryTable) :
* Four Top Decay: 
    * Primary Dataset: /store/mc/RunIIFall17NanoAOD/TTTT_TuneCP5_13TeV-amcatnlo-pythia8/
    * NANOAODSIM/
    * Campaign: RunIIFall17NanoAOD/
    * Process String: PU2017_12Apr2018_94X_mc2017_realistic_v14-v1
        * Processing Version: v1
* TTBar Decay: 
    * /store/mc/RunIIFall17NanoAOD/TTJets_SingleLeptFromT_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/
    PU2017_12Apr2018_94X_mc2017_realistic_v14-v1
    
### HLTriggers
This study is done using non-prescaled HLT triggers, which can be checked by searching the HLT menu at the [CMS-HLT 
configuration explorer](https://cmsweb.cern.ch/confdb/). The HLT Menu names/paths for 2017-18 can be found at:
* [TopTrigger2018](https://twiki.cern.ch/twiki/bin/view/CMS/TopTriggerYear2017) (last updated 2018-09-27) and
* [TopTrigger2017](https://twiki.cern.ch/twiki/bin/view/CMS/TopTriggerYear2018) (last updated 2018-09-12) .

Currently the triggers which are being studied, in the hopes that a better event acceptance efficiency can be achieved, 
are:
* IsoMu24  ,
* PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2  and
* Mu15_IsoVVVL_PFHT450_CaloBTagCSV_4p5  ,

where if a combination is successful it will be called: IsoMu24_PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2 .

### Jet Acceptance Criteria
Jets are counted if the following criteria are satisfied:
* Must satisfy what is called a JetID > 2 (https://twiki.cern.ch/twiki/bin/view/CMS/JetID13TeVRun2017),
* Momentum pT of at least 30 GeV
* Absolute value of pseudo-rapidity (eta) less than 2.4  
* Implement jet cleaning (”cleanmask”) , with priority given to leptons

If Jet passes above criteria it is counted as a b-tagged jet if:
* At least one of these Jets that pass the above criteria are from b-quarks, checked by b-tagging algorithms, at the
moment it required that the value given by the DeepFlavourB algorithm is larger than 0.7489 
(https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation94X), which is recognised as a tight test.


### Muon Acceptance Criteria
Muons are counted if the following criteria are satisfied:
* Absolute value of pseudo-rapidity (eta) less than 2.4 
* Relatively well isolated, in other words not very close to other particles that may inhibit the its 
correct identification or the measure of its properties. This is done using an algorithm that tests the total particle 
flow relative isolation, the particular one used is called miniPFRelIso_all and should give a value less than 0.15.
* Correctly identified, in other words not mistakenly identified another particle as a muon; this is done using special
algorithms. In this study, one such algorithm was used, which only accepts particles identified as muons with high
certainty [(known as tightId)](https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideMuonIdRun2).

### Electron Acceptance Criteria
Electrons are counted if the following criteria are satisfied:
* Absolute value of pseudo-rapidity (eta) less than 2.4, but with a vetoed section from 1.4442 to 1.566;
* i.e. Electrons are counted if in the regions : |η|<1.4442 and 1.566<|η|<2.4

### Denominator of “Trigger Efficiencies”
Accepted Events:
* Six or more jets pass the jet criteria,
* Two of which are b-tagged,
* One muon passes the muon criteria and • Zero electrons pass the electron criteria

<detail>
 <summary> Numerator of “Trigger Efficiencies”</summary>
 <br>
Accepted Events:
* If the Denominator criteria are satisfied and • thegivenTriggerstudiedis“True”.
Un-Prescaled Triggers studied for μ + jets:
* 'IsoMu24’
* 'PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2’
* Combined Version: ' 'IsoMu24 _PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2’ • ‘Mu15_IsoVVVL_PFHT450_CaloBTagCSV_4p5’

 </br>
</detail>
<detail>
<summary>Instructions for Repeating Study:</summary>
 <br> 
 To produce a text file of [triggers](https://twiki.cern.ch/twiki/bin/view/CMS/TriggerStudies)
( and other unwanted stuff, which will be removed) do:
<pre>
    $ HLTnames.py | tee LeafNames.txt
</pre>
or 
<pre>
    $ HLTnames.py > LeafNames.txt
</pre>
To produce histograms run:
<pre>
    $ python3 nsMain.py
</pre>
which imports histoMaker and adds HistogramMaker() as an argument to the postProcessor. 
The choice of triggers is given here, along with the preselection criteria.

The help message given for [`histoMain.py`](histoMain.py) is:
<pre>
usage: nsMain.py [-h] [-f {ttjets,tttt,tttt_weights,wjets}]
                 [-r {xrd-global,xrdUS,xrdEU_Asia,eos,iihe,local}] [-nw]
                 [-e EVENTLIMIT]

optional arguments:
  -h, --help            show this help message and exit
  -f {ttjets,tttt,tttt_weights,wjets}, --inputLFN {ttjets,tttt,tttt_weights,wjets}
                        Set list of input files (default: tttt)
  -r {xrd-global,xrdUS,xrdEU_Asia,eos,iihe,local}, --redirector {xrd-global,xrdUS,xrdEU_Asia,eos,iihe,local}
                        Sets redirector to query locations for LFN (default:
                        local)
  -nw, --noWriteFile    Does not output a ROOT file, which contains the
                        histograms. (default: False)
  -e EVENTLIMIT, --eventLimit EVENTLIMIT
                        Set a limit to the number of events. (default: -1)
</pre>
___

To produce [`histoDraw.py`](histoDraw.py) plots run:
<pre>
    $ python histoDraw.py
</pre>

The help nessage given for [`histoDraw.py`](histoDraw.py) is:
<pre>
usage: histoDraw.py [-h] [-f {ttjets,tttt,tttt_weights,wjets}]

optional arguments:
  -h, --help            show this help message and exit
  -f {ttjets,tttt,tttt_weights,wjets}, --inputLFN {ttjets,tttt,tttt_weights,wjets}
                        Set list of input files (default: tttt)
</pre>

I will try to introduce the option to input a trigger as an argument to some of these 
and if argument is not given it will revert to search for a default trigger 
and exit if trigger does not exist.
At the moment it makes more sense not to introduce command line args for triggers as 
this code is only used by me!

</br>
</detail>

<details>
<summary>How do I dropdown?</summary>
<br>
This is how you dropdown.
<br><br>
<pre>
&lt;details&gt;
&lt;summary&gt;How do I dropdown?&lt;/summary&gt;
&lt;br&gt;
This is how you dropdown.
&lt;details&gt;
$ HLTnames.py | tee LeafNames.txt
</pre>
</details>

---

<details open>
<summary>Want to ruin the surprise?</summary>
<br>
Well, you asked for it!
<br><br>
<pre>
&lt;details open&gt;
&lt;summary&gt;Want to ruin the surprise?&lt;/summary&gt;
&lt;br&gt;
Well, you asked for it!
&lt;details&gt;
</pre>
</details>

<details>
<summary>Heading</summary>
<ul>
<li> markdown list 1</li>
<ul>
<li> nested list 1</li>
<li> nested list 2</li>
</ul>
<li> markdown list 2</li>
</ul>
</details>

<details>
<summary>Heading</summary>

+ markdown list 1
    + nested list 1
    + nested list 2
+ markdown list 2

</details>

 </br>
</details> 
or 

```
    $ HLTnames.py > LeafNames.txt
```

To produce histograms run:
```
    $ python3 nsMain.py
```
which imports histoMaker and adds HistogramMaker() as an argument to the postProcessor. 
The choice of triggers is given here, along with the preselection criteria.

The help message given for [`histoMain.py`](histoMain.py) is:
```
usage: nsMain.py [-h] [-f {ttjets,tttt,tttt_weights,wjets}]
                 [-r {xrd-global,xrdUS,xrdEU_Asia,eos,iihe,local}] [-nw]
                 [-e EVENTLIMIT]

optional arguments:
  -h, --help            show this help message and exit
  -f {ttjets,tttt,tttt_weights,wjets}, --inputLFN {ttjets,tttt,tttt_weights,wjets}
                        Set list of input files (default: tttt)
  -r {xrd-global,xrdUS,xrdEU_Asia,eos,iihe,local}, --redirector {xrd-global,xrdUS,xrdEU_Asia,eos,iihe,local}
                        Sets redirector to query locations for LFN (default:
                        local)
  -nw, --noWriteFile    Does not output a ROOT file, which contains the
                        histograms. (default: False)
  -e EVENTLIMIT, --eventLimit EVENTLIMIT
                        Set a limit to the number of events. (default: -1)
```
___

To produce [`histoDraw.py`](histoDraw.py) plots run:
```
    $ python histoDraw.py
```

The help nessage given for [`histoDraw.py`](histoDraw.py) is:
```
usage: histoDraw.py [-h] [-f {ttjets,tttt,tttt_weights,wjets}]

optional arguments:
  -h, --help            show this help message and exit
  -f {ttjets,tttt,tttt_weights,wjets}, --inputLFN {ttjets,tttt,tttt_weights,wjets}
                        Set list of input files (default: tttt)
```

I will try to introduce the option to input a trigger as an argument to some of these 
and if argument is not given it will revert to search for a default trigger 
and exit if trigger does not exist.
At the moment it makes more sense not to introduce command line args for triggers as 
this code is only used by me!

