import os, errno
import ROOT
from ROOT import TLatex
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from datetime import datetime

def process_arguments():
    """ Process command-line arguments """

    parser = ArgumentParser(description=__doc__, formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-f", "--inputLFN", choices= ["ttjets","tttt", "tttt_weights", "wjets"],
                        default = "tttt", help= "Set list of input files")
    args = parser.parse_args()
    return args

def pdfCreator(arg, canvas):
    time_ = datetime.now()
    filename = time_.strftime("TriggerPlots/W%V_%y/%w%a.pdf")
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise
    if arg == 0: canvas.Print(time_.strftime("TriggerPlots/W%V_%y/%w%a.pdf("),"pdf")
    if arg == 1: canvas.Print(time_.strftime("TriggerPlots/W%V_%y/%w%a.pdf"),"pdf")
    if arg == 2: canvas.Print(time_.strftime("TriggerPlots/W%V_%y/%w%a.pdf)"),"pdf")

def main(argms):
    """ This code merges histograms, only for specific root file """

    if argms.inputLFN == "ttjets":
        inputFile = "OutHistosTT6jets.root"
    elif argms.inputLFN == "tttt_weights":
        inputFile = "OutHistosTTTTweights.root"
    elif argms.inputLFN == "wjets":
        inputFile = "OutHistosWjets.root"
    elif argms.inputLFN == "tttt":
        inputFile = "TestOutHistosTTTT_6jets.root"
    else:
        return 0
    
    # - Initialise variables
    trigList = {"combos":['IsoMu24_PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2'],
                "stndlone":['Mu15_IsoVVVL_PFHT450_CaloBTagCSV_4p5'],
                "t1" :['IsoMu24'],
                "t2":['PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2']}

    h_jetHt = {}
    h_jetEta = {}
    h_jetPhi ={}
    h_jetMap = {}
    h_muonPt = {}
    h_muonEta = {}
    h_muonPhi = {}
    h_muonMap = {}
    h_jetHtTriggerRatio ={}
    h_muoPtTriggerRatio = {}

    # - Create canvases
    triggerCanvas = ROOT.TCanvas('triggerCanvas', 'Triggers', 1100,600)
    #triggerCanvas.Divide(2,1)

    # - Open file and sub folder
    histFile = ROOT.TFile.Open(inputFile)
    histFile.cd("plots")

    # - Jet HT histograms
    h_jetHt["notrigger"] = ROOT.gDirectory.Get("h_jetHt_notrigger")
    h_jetHt["notrigger"].SetLineColor(1)
    if not (h_jetHt["notrigger"]):
        print("No trigger jet Ht histogram is empty")
    h_jetEta["notrigger"] = ROOT.gDirectory.Get("h_jetEta_notrigger")
    h_jetEta["notrigger"].SetLineColor(1)
    if not (h_jetEta["notrigger"]):
        print("No trigger jet Eta histogram is empty")
    h_jetPhi["notrigger"] = ROOT.gDirectory.Get("h_jetPhi_notrigger")
    h_jetPhi["notrigger"].SetLineColor(1)
    if not (h_jetPhi["notrigger"]):
        print("No trigger jet Phi histogram is empty")
    h_jetMap["notrigger"] = ROOT.gDirectory.Get("h_jetMap_notrigger")
    h_jetMap["notrigger"].SetLineColor(1)
    if not (h_jetMap["notrigger"]):
        print("No trigger jet map histogram is empty")
    h_muonPt["notrigger"] = ROOT.gDirectory.Get("h_muonPt_notrigger")
    h_muonPt["notrigger"].SetLineColor(1)
    if not (h_muonPt["notrigger"]):
        print("No trigger muon Pt histogram is empty")
    h_muonEta["notrigger"] = ROOT.gDirectory.Get("h_muonEta_notrigger")
    h_muonEta["notrigger"].SetLineColor(1)
    if not (h_muonEta["notrigger"]):
        print("No trigger muon eta histogram is empty")
    h_muonPhi["notrigger"] = ROOT.gDirectory.Get("h_muonPhi_notrigger")
    h_muonPhi["notrigger"].SetLineColor(1)
    if not (h_muonPhi["notrigger"]):
        print("No trigger muon Phi histogram is empty")
    h_muonMap["notrigger"] = ROOT.gDirectory.Get("h_muonMap_notrigger")
    h_muonMap["notrigger"].SetLineColor(1)
    if not (h_muonMap["notrigger"]):
        print("No trigger muon map histogram is empty")

    i=2
    for key in trigList:
        for tg in trigList[key]:
            h_jetHt[tg] = ROOT.gDirectory.Get("h_jetHt_" + tg)
            h_jetEta[tg] = ROOT.gDirectory.Get("h_jetEta_" + tg)
            h_jetPhi[tg] = ROOT.gDirectory.Get("h_jetPhi_" + tg)
            h_jetMap[tg] = ROOT.gDirectory.Get("h_jetMap_" + tg)
            h_muonPt[tg] = ROOT.gDirectory.Get("h_muonPt_" + tg)
            h_muonEta[tg] = ROOT.gDirectory.Get("h_muonEta_" + tg)
            h_muonPhi[tg] = ROOT.gDirectory.Get("h_muonPhi_" + tg)
            h_muonMap[tg] = ROOT.gDirectory.Get("h_muonMap_" + tg)

            h_jetHt[tg].SetLineColor(i)
            h_jetEta[tg].SetLineColor(i)
            h_jetPhi[tg].SetLineColor(i)
            h_muonPt[tg].SetLineColor(i)
            h_muonEta[tg].SetLineColor(i)
            h_muonPhi[tg].SetLineColor(i)

            i+=1

    # - Events histogram
    h_eventsPrg = ROOT.gDirectory.Get("h_eventsPrg")
    if not (h_eventsPrg):
        print("h_eventsPrg histogram is empty")
        return 

    ####################
    # - Draw on Canvas #
    ####################
    # - Canvas Details
    triggerCanvas.cd(1)
    l = TLatex()                                                                                                                                                         
    l.DrawLatex(0.10, 0.70, "On-line (pre-)selection Requisites for:")
    l.DrawLatex(0.16, 0.65, "#bullet Jets: #bf{number > 5 , jetId > 2 and |#eta| < 2.4 }")
    l.DrawLatex(0.16, 0.60, "#bullet Muons: #bf{number >0 and has softId}")
    l.DrawLatex(0.10, 0.50, "Event Limit: #bf{None (see last page)}")
    l.DrawLatex(0.10, 0.40, "Off-line (post-)selection Requisites for:")
    l.DrawLatex(0.16, 0.35, "#bullet Jets: #bf{jetId > 2 , p_{T} > 30 and |#eta|<2.4 (for at least 6)}")
    l.DrawLatex(0.16, 0.30, "      #bf{btagDeepFlavB > 0.7489 (for at least one jet)}")
    l.DrawLatex(0.16, 0.25, "#bullet Muons: #bf{has tightId, |#eta|<2.4 and miniPFRelIso_all<0.15 (for at least 1)}")
    l.SetTextSize(0.015)
    pdfCreator(0,triggerCanvas)

    # - HT plots ---------------------------------
    cv1=triggerCanvas.cd(1)
    #h_jetHt["notrigger"].GetYaxis().SetTitleOffset(1.5)
    h_jetHt["notrigger"].Draw()
    for key in trigList:
        for tg in trigList[key]:
            h_jetHt[tg].Draw('same')
    cv1.BuildLegend(0.4,0.3,0.4,0.3)
    #leg1.SetNColumns(2)
    ROOT.gStyle.SetLegendTextSize(0.02)
    tX1 = 0.04*(h_jetHt["notrigger"].GetXaxis().GetXmax())
    tY1 = 0.95*(h_jetHt["notrigger"].GetMaximum())
    l.SetTextSize(0.03)
    l.DrawLatex(tX1,tY1,"#splitline{CMS}{t#bar{t} #rightarrow l #nu_{l} #plus jets}")
    pdfCreator(1,triggerCanvas)

    cv2=triggerCanvas.cd(1)
    i=0
    for tg in trigList["combos"]:
        h_jetHtTriggerRatio[tg] = (h_jetHt[tg]).Clone("h_jetHtRatio" + tg)
        h_jetHtTriggerRatio[tg].Divide(h_jetHt["notrigger"])
        if  i==0: 
            h_jetHtTriggerRatio[tg].Draw()
            tX1 = 0.04*(h_jetHtTriggerRatio[tg].GetXaxis().GetXmax())
            tY1 = 0.95*(h_jetHtTriggerRatio[tg].GetMaximum())
        if  i==1: h_jetHtTriggerRatio[tg].Draw('same')
        i += 1
    for tg in trigList["stndlone"]:
        h_jetHtTriggerRatio[tg] = (h_jetHt[tg]).Clone("h_jetHtRatio" + tg)
        h_jetHtTriggerRatio[tg].Divide(h_jetHt["notrigger"])
        if  i==0: 
            h_jetHtTriggerRatio[tg].Draw()
            tX1 = 0.04*(h_jetHtTriggerRatio[tg].GetXaxis().GetXmax())
            tY1 = 0.95*(h_jetHtTriggerRatio[tg].GetMaximum())
        if  i==1: h_jetHtTriggerRatio[tg].Draw('same')
        i += 1

    cv2.BuildLegend(0.4,0.3,0.4,0.3)
    ROOT.gStyle.SetLegendTextSize(0.02)
    l.SetTextSize(0.03)
    l.DrawLatex(tX1,tY1,"#splitline{CMS}{t#bar{t} #rightarrow l #nu_{l} #plus jets}")
    pdfCreator(1,triggerCanvas)

    # - pT plots ---------------------------------
    cv3=triggerCanvas.cd(1)
    #h_muonPt["notrigger"].GetYaxis().SetTitleOffset(1.5)
    h_muonPt["notrigger"].Draw()
    tX1 = 0.04*(h_muonPt["notrigger"].GetXaxis().GetXmax())
    tY1 = 0.95*(h_muonPt["notrigger"].GetMaximum())
    for key in trigList:
        for tg in trigList[key]:
            h_muonPt[tg].Draw('same')
    cv3.BuildLegend(0.4,0.3,0.4,0.3)
    l.SetTextSize(0.03)
    l.DrawLatex(tX1,tY1,"#splitline{CMS}{t#bar{t} #rightarrow l #nu_{l} #plus jets}")
    ROOT.gStyle.SetLegendTextSize(0.02)
    pdfCreator(1,triggerCanvas)

    cv4=triggerCanvas.cd(1)
    i=0
    for tg in trigList["combos"]:
        h_muoPtTriggerRatio[tg] = (h_muonPt[tg]).Clone("h_muonPtRatio" + tg)
        h_muoPtTriggerRatio[tg].Divide(h_muonPt["notrigger"])
        if i == 0 :
            h_muoPtTriggerRatio[tg].Draw()
            tX1 = 0.04*(h_muoPtTriggerRatio[tg].GetXaxis().GetXmax())
            tY1 = 0.95*(h_muoPtTriggerRatio[tg].GetMaximum())
        if i == 1 :h_muoPtTriggerRatio[tg].Draw('same')
        i += 1
    for tg in trigList["stndlone"]:
        h_muoPtTriggerRatio[tg] = (h_muonPt[tg]).Clone("h_muonPtRatio" + tg)
        h_muoPtTriggerRatio[tg].Divide(h_muonPt["notrigger"])
        if i == 0 :
            h_muoPtTriggerRatio[tg].Draw()
            tX1 = 0.04*(h_muoPtTriggerRatio[tg].GetXaxis().GetXmax())
            tY1 = 0.95*(h_muoPtTriggerRatio[tg].GetMaximum())
        if i == 1 :h_muoPtTriggerRatio[tg].Draw('same')
        i += 1
    cv4.BuildLegend(0.4,0.3,0.4,0.3)
    ROOT.gStyle.SetLegendTextSize(0.02)
    l.SetTextSize(0.03)
    l.DrawLatex(tX1,tY1,"#splitline{CMS}{t#bar{t} #rightarrow l #nu_{l} #plus jets}")
    pdfCreator(1,triggerCanvas)

    # - Eta plots ------------------------------------------
    cv5=triggerCanvas.cd(1)
    #h_jetEta["notrigger"].GetYaxis().SetTitleOffset(1.1)
    h_jetEta["notrigger"].Draw()
    tX1 = 0.94*(-6)
    tY1 = 0.95*(h_jetEta["notrigger"].GetMaximum())
    for key in trigList:
        for tg in trigList[key]:
            h_jetEta[tg].Draw('same')
    cv5.BuildLegend(0.4,0.3,0.4,0.3)
    l.SetTextSize(0.03)
    l.DrawLatex(tX1,tY1,"#splitline{CMS}{t#bar{t} #rightarrow l #nu_{l} #plus jets}")
    ROOT.gStyle.SetLegendTextSize(0.02)
    pdfCreator(1,triggerCanvas)

    cv6=triggerCanvas.cd(1)
    #h_muonEta["notrigger"].GetYaxis().SetTitleOffset(1.2)
    h_muonEta["notrigger"].Draw()
    tX1 = 0.94*(-6)
    tY1 = 0.95*(h_muonEta["notrigger"].GetMaximum())
    for key in trigList:
        for tg in trigList[key]:
            h_muonEta[tg].Draw('same')
    cv6.BuildLegend(0.4,0.3,0.4,0.3)
    l.SetTextSize(0.03)
    l.DrawLatex(tX1,tY1,"#splitline{CMS}{t#bar{t} #rightarrow l #nu_{l} #plus jets}")
    ROOT.gStyle.SetLegendTextSize(0.02)
    pdfCreator(1,triggerCanvas)


    # - Phi plots ------------------------------------------
    cv7=triggerCanvas.cd(1)
    #h_jetPhi["notrigger"].GetYaxis().SetTitleOffset(1.3)
    h_jetPhi["notrigger"].Draw()
    tX1 = 0.94*(-6)
    tY1 = 0.95*(h_jetPhi["notrigger"].GetMaximum())
    for key in trigList:
        for tg in trigList[key]:
            h_jetPhi[tg].Draw('same')
    cv7.BuildLegend(0.4,0.3,0.4,0.3)
    l.SetTextSize(0.03)
    l.DrawLatex(tX1,tY1,"#splitline{CMS}{t#bar{t} #rightarrow l #nu_{l} #plus jets}")
    ROOT.gStyle.SetLegendTextSize(0.02)
    pdfCreator(1,triggerCanvas)

    cv8=triggerCanvas.cd(1)
    #h_muonPhi["notrigger"].GetYaxis().SetTitleOffset(1.4)
    h_muonPhi["notrigger"].Draw()
    tX1 = 0.94*(-6)
    tY1 = 0.97*(h_muonPhi["notrigger"].GetMaximum())
    for key in trigList:
        for tg in trigList[key]:
            h_muonPhi[tg].Draw('same')
    cv8.BuildLegend(0.4,0.3,0.4,0.3)
    l.SetTextSize(0.03)
    l.DrawLatex(tX1,tY1,"#splitline{CMS}{t#bar{t} #rightarrow l #nu_{l} #plus jets}")
    ROOT.gStyle.SetLegendTextSize(0.02)
    pdfCreator(1,triggerCanvas)

    # - Eta-Phi Map plots ------------------------------------------
    triggerCanvas.cd(1)
    h_jetMap["notrigger"].Draw('SURF1')#CONT4Z
    pdfCreator(1,triggerCanvas)
    for key in trigList:
        for tg in trigList[key]:
            h_jetMap[tg].Draw('SURF1')
            pdfCreator(1,triggerCanvas)

    h_muonMap["notrigger"].Draw('SURF1')
    pdfCreator(1,triggerCanvas)
    for key in trigList:
        for tg in trigList[key]:
            h_muonMap[tg].Draw('SURF1')#E
            pdfCreator(1,triggerCanvas)

    # - Test Event numbers along steps ----------
    triggerCanvas.cd(1)
    h_eventsPrg.Draw()
    tY1 = 0.05*(h_eventsPrg.GetMaximum())
    l.SetTextAngle(80)
    l.DrawLatex(0.5,tY1,"Pre-selection")
    l.DrawLatex(1.5,tY1,"Post-selection")
    pdfCreator(2,triggerCanvas)

    histFile.Close()

main(process_arguments())
