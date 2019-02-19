import os
import errno
import ROOT
from ROOT import TLatex
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from datetime import datetime


def process_arguments():
    """ Process command-line arguments """

    parser = ArgumentParser(description=__doc__, formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-f", "--inputLFN", choices=["ttjets", "tttt", "tttt_weights", "wjets"],
                        default="tttt", help="Set list of input files")
    args = parser.parse_args()
    return args


def pdfCreator(parg, arg, canvas):
    """
           Create a pdf of histograms
           Args:
               parg (class): commandline arguments
               arg (int): print argument
               canvas (TCanvas): canvas which includes plot
    """
    time_ = datetime.now()
    filename = time_.strftime("TriggerPlots/W%V_%y/%w%a_" + parg.inputLFN + ".pdf")
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise
    if arg == 0:
        canvas.Print(time_.strftime("TriggerPlots/W%V_%y/%w%a_" + parg.inputLFN + ".pdf("), "pdf")
    if arg == 1:
        canvas.Print(time_.strftime("TriggerPlots/W%V_%y/%w%a_" + parg.inputLFN + ".pdf"), "pdf")
    if arg == 2:
        canvas.Print(time_.strftime("TriggerPlots/W%V_%y/%w%a_" + parg.inputLFN + ".pdf)"), "pdf")


def main(argms):
    """ This code merges histograms, only for specific root file """

    if argms.inputLFN == "ttjets":
        inputFile = "../OutFiles/Histograms/TT6jets2.root"
    elif argms.inputLFN == "tttt_weights":
        inputFile = "../OutFiles/Histograms/TTTTweights.root"
    elif argms.inputLFN == "wjets":
        inputFile = "../OutFiles/Histograms/Wjets.root"
    elif argms.inputLFN == "tttt":
        inputFile = "../OutFiles/Histograms/TTTT_6jets2.root"
    else:
        return 0

    trigList = {}
    with open("trigList.txt") as f:
        for line in f:
            if line.find(":") == -1: continue
            (key1, val) = line.split(": ")
            c = len(val) - 1
            val = val[0:c]
            trigList[key1] = val.split(", ")

    preSelCuts = {}
    with open("../preSelectionCuts.txt") as f:
        for line in f:
            if line.find(":") == -1: continue
            (key1, val) = line.split(": ")
            c = len(val) - 1
            val = val[0:c]
            preSelCuts[key1] = val

    selCriteria = {}
    with open("selectionCriteria.txt") as f:
        for line in f:
            if line.find(":") == -1: continue
            (key1, val) = line.split(": ")
            c = len(val) - 1
            val = val[0:c]
            selCriteria[key1] = val

    h_jetHt = {}
    h_jetMult = {}
    h_jetBMult = {}
    h_jetEta = {}
    h_jetPhi = {}
    h_jetMap = {}

    h_elPt = {}
    h_elEta = {}
    h_elPhi = {}
    h_elMap = {}
    h_metPt = {}
    h_metPhi = {}
    h_genMetPt = {}
    h_genMetPhi = {}

    h_TriggerRatio = {}

    # - Create canvases
    triggerCanvas = ROOT.TCanvas('triggerCanvas', 'Triggers', 1100, 600)

    # - Open file and sub folder
    histFile = ROOT.TFile.Open(inputFile)
    histFile.cd("plots")

    # - Histograms
    h_jetHt["notrigger"] = ROOT.gDirectory.Get("h_jetHt_notrigger")
    h_jetHt["notrigger"].SetLineColor(1)
    if not (h_jetHt["notrigger"]):
        print("No trigger jet Ht histogram is empty")
    h_jetMult["notrigger"] = ROOT.gDirectory.Get("h_jetMult_notrigger")
    h_jetMult["notrigger"].SetLineColor(1)
    if not (h_jetMult["notrigger"]):
        print("No trigger jet Mult histogram is empty")
    h_jetBMult["notrigger"] = ROOT.gDirectory.Get("h_jetBMult_notrigger")
    h_jetBMult["notrigger"].SetLineColor(1)
    if not (h_jetBMult["notrigger"]):
        print("No trigger jet BMult histogram is empty")
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

    h_elMiniPfRelIso_all = ROOT.gDirectory.Get("h_elMiniPfRelIso_all")
    h_elGenPartFlav = ROOT.gDirectory.Get("h_elGenPartFlav")
    h_elGenPartIdx = ROOT.gDirectory.Get("h_elGenPartIdx")
    h_elPt["prompt"] = ROOT.gDirectory.Get("h_elPt_prompt")
    h_elPt["prompt"].SetLineColor(4)
    if not (h_elPt["prompt"]):
        print("Prompt Electron Pt histogram is empty")
    h_elPt["non-prompt"] = ROOT.gDirectory.Get("h_elPt_non-prompt")
    h_elPt["non-prompt"].SetLineColor(2)
    if not (h_elPt["non-prompt"]):
        print("Bottom mother muon Pt histogram is empty")

    h_elPt["notrigger"] = ROOT.gDirectory.Get("h_elPt_notrigger")
    h_elPt["notrigger"].SetLineColor(1)
    if not (h_elPt["notrigger"]):
        print("No trigger el Pt histogram is empty")
    h_elEta["notrigger"] = ROOT.gDirectory.Get("h_elEta_notrigger")
    h_elEta["notrigger"].SetLineColor(1)
    if not (h_elEta["notrigger"]):
        print("No trigger el eta histogram is empty")
    h_elPhi["notrigger"] = ROOT.gDirectory.Get("h_elPhi_notrigger")
    h_elPhi["notrigger"].SetLineColor(1)
    if not (h_elPhi["notrigger"]):
        print("No trigger el Phi histogram is empty")
    h_elMap["notrigger"] = ROOT.gDirectory.Get("h_elMap_notrigger")
    h_elMap["notrigger"].SetLineColor(1)
    if not (h_elMap["notrigger"]):
        print("No trigger el map histogram is empty")

    h_metPt["notrigger"] = ROOT.gDirectory.Get("h_metPt_notrigger")
    h_metPt["notrigger"].SetLineColor(1)
    if not (h_metPt["notrigger"]):
        print("No trigger met Pt histogram is empty")
    h_metPhi["notrigger"] = ROOT.gDirectory.Get("h_metPhi_notrigger")
    h_metPhi["notrigger"].SetLineColor(1)
    if not (h_metPhi["notrigger"]):
        print("No trigger met Phi histogram is empty")

    h_genMetPt["notrigger"] = ROOT.gDirectory.Get("h_genMetPt_notrigger")
    h_genMetPt["notrigger"].SetLineColor(1)
    if not (h_genMetPt["notrigger"]):
        print("No trigger genMet Pt histogram is empty")
    h_genMetPhi["notrigger"] = ROOT.gDirectory.Get("h_genMetPhi_notrigger")
    h_genMetPhi["notrigger"].SetLineColor(1)
    if not (h_genMetPhi["notrigger"]):
        print("No trigger genMet Phi histogram is empty")

    i = 2
    for key in trigList:
        if not key.find("Mu") == -1: continue
        for tg in trigList[key]:
            h_jetHt[tg] = ROOT.gDirectory.Get("h_jetHt_" + tg)
            h_jetMult[tg] = ROOT.gDirectory.Get("h_jetMult_" + tg)
            h_jetBMult[tg] = ROOT.gDirectory.Get("h_jetBMult_" + tg)
            h_jetEta[tg] = ROOT.gDirectory.Get("h_jetEta_" + tg)
            h_jetPhi[tg] = ROOT.gDirectory.Get("h_jetPhi_" + tg)
            h_jetMap[tg] = ROOT.gDirectory.Get("h_jetMap_" + tg)

            h_elPt[tg] = ROOT.gDirectory.Get("h_elPt_" + tg)
            h_elEta[tg] = ROOT.gDirectory.Get("h_elEta_" + tg)
            h_elPhi[tg] = ROOT.gDirectory.Get("h_elPhi_" + tg)
            h_elMap[tg] = ROOT.gDirectory.Get("h_elMap_" + tg)

            h_metPt[tg] = ROOT.gDirectory.Get("h_metPt_" + tg)
            h_metPhi[tg] = ROOT.gDirectory.Get("h_metPhi_" + tg)
            h_genMetPt[tg] = ROOT.gDirectory.Get("h_genMetPt_" + tg)
            h_genMetPhi[tg] = ROOT.gDirectory.Get("h_genMetPhi_" + tg)

            h_jetHt[tg].SetLineColor(i)
            h_jetMult[tg].SetLineColor(i)
            h_jetBMult[tg].SetLineColor(i)
            h_jetEta[tg].SetLineColor(i)
            h_jetPhi[tg].SetLineColor(i)
            h_elPt[tg].SetLineColor(i)
            h_elEta[tg].SetLineColor(i)
            h_elPhi[tg].SetLineColor(i)
            h_metPt[tg].SetLineColor(i)
            h_metPhi[tg].SetLineColor(i)
            h_genMetPt[tg].SetLineColor(i)
            h_genMetPhi[tg].SetLineColor(i)

            i += 1

    # - Events histogram
    h_eventsPrg = ROOT.gDirectory.Get("h_eventsPrg")
    if not h_eventsPrg:
        print("h_eventsPrg histogram is empty")
        return

    ####################
    # - Draw on Canvas #
    ####################
    # - Canvas Details
    triggerCanvas.cd(1)
    ltx = TLatex()
    ltx.DrawLatex(0.10, 0.70, "On-line (pre-)selection Requisites for:")
    ltx.DrawLatex(0.16, 0.65, "#bullet Jets: #bf{number > %s}" % preSelCuts["nJet"])
    ltx.DrawLatex(0.16, 0.60, "#bullet Muons plus Electrons: #bf{number > %s }" % preSelCuts["nLepton"])
    ltx.DrawLatex(0.10, 0.50, "Event Limit: #bf{None (see last page)}")
    ltx.DrawLatex(0.10, 0.40, "Off-line (post-)selection Requisites for:")
    ltx.DrawLatex(0.16, 0.35, "#bullet Jets: #bf{jetId > %s , p_{T} > %s and |#eta|<%s (for at least 6 jets)}"
                  % (selCriteria["minJetId"], selCriteria["minJetPt"], selCriteria["maxObjEta"]))
    ltx.DrawLatex(0.16, 0.30, "      #bf{btagDeepFlavB > 0.7489 (for at least one jet)}")
    ltx.DrawLatex(0.16, 0.25, "#bullet Muons: #bf{has tightId, |#eta|<%s and miniPFRelIso_all<%s (for at least 1)}"
                  % (selCriteria["maxObjEta"], selCriteria["maxPfRelIso"]))
    ltx.SetTextSize(0.015)
    pdfCreator(argms, 0, triggerCanvas)

    # - Create text for legend
    if argms.inputLFN == "ttjets":
        legString = "#splitline{CMS}{t#bar{t} #rightarrow l #nu_{l} #plus jets}"
    elif argms.inputLFN == "tttt":
        legString = "#splitline{CMS}{t#bar{t}t#bar{t} #rightarrow l #nu_{l} #plus jets}"
    elif argms.inputLFN == "tttt_weights":
        legString = "#splitline{CMS}{t#bar{t}t#bar{t} #rightarrow l #nu_{l} #plus jets}"
    else:
        legString = "#splitline{CMS}{W #rightarrow jets}"

    ROOT.gStyle.SetOptTitle(0)

    # - HT plots for mu Triggers ---------------------------------
    cv1 = triggerCanvas.cd(1)
    h_jetHt["notrigger"].Draw('E1')
    for key in trigList:
        if not key.find("Mu") == -1: continue
        for tg in trigList[key]:
            h_jetHt[tg].Draw('E1 same')
    cv1.BuildLegend(0.57, 0.54, 0.97, 0.74)
    ROOT.gStyle.SetLegendTextSize(0.02)
    tX1 = 0.6*(h_jetHt["notrigger"].GetXaxis().GetXmax())
    tY1 = 0.95*(h_jetHt["notrigger"].GetMaximum())
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    pdfCreator(argms, 1, triggerCanvas)

    cv2 = triggerCanvas.cd(1)
    i = 0
    j = 2
    for key in trigList:
        if not key.find("Mu") == -1: continue
        for tg in trigList[key]:
            if ROOT.TEfficiency.CheckConsistency(h_jetHt[tg], h_jetHt["notrigger"]):
                h_TriggerRatio[tg] = ROOT.TEfficiency(h_jetHt[tg], h_jetHt["notrigger"])
                xTitle = h_jetHt["notrigger"].GetXaxis().GetTitle()
                xBinWidth = h_jetHt["notrigger"].GetXaxis().GetBinWidth(1)
                h_TriggerRatio[tg].SetTitle(";{0};Trigger Efficiency per {1}GeV/c".format(xTitle, round(xBinWidth)))
                h_TriggerRatio[tg].SetName(tg)
                h_TriggerRatio[tg].SetTitle(tg)
                h_TriggerRatio[tg].SetLineColor(j)
                j += 1
                if i == 0:
                    h_TriggerRatio[tg].Draw('AP')
                    cv2.Update()
                    graph1 = h_TriggerRatio[tg].GetPaintedGraph()
                    graph1.SetMinimum(0)
                    graph1.SetMaximum(1.2)
                    cv2.Update()
                    tX1 = 0.05*(h_jetHt["notrigger"].GetXaxis().GetXmax())
                    tY1 = 1.1
                if i > 0:
                    h_TriggerRatio[tg].Draw('same')
            i += 1
    cv2.BuildLegend(0.5, 0.1, 0.9, 0.3)
    ROOT.gStyle.SetLegendTextSize(0.02)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    pdfCreator(argms, 1, triggerCanvas)

    # - Jet Multiplicity plots ---------------------------------
    cv3 = triggerCanvas.cd(1)
    h_jetMult["notrigger"].GetXaxis().SetTitle("Number of Jets")
    h_jetMult["notrigger"].Draw('E1')
    for key in trigList:
        if not key.find("Mu") == -1: continue
        for tg in trigList[key]:
            h_jetMult[tg].Draw('E1 same')
    cv3.BuildLegend(0.57, 0.54, 0.97, 0.74)
    ROOT.gStyle.SetLegendTextSize(0.02)
    tX1 = 0.6 * (h_jetMult["notrigger"].GetXaxis().GetXmax())
    tY1 = 0.95 * (h_jetMult["notrigger"].GetMaximum())
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    pdfCreator(argms, 1, triggerCanvas)

    cv4 = triggerCanvas.cd(1)
    i = 0
    j = 2
    for key in trigList:
        if not key.find("Mu") == -1: continue
        for tg in trigList[key]:
            if ROOT.TEfficiency.CheckConsistency(h_jetMult[tg], h_jetMult["notrigger"]):
                h_TriggerRatio[tg] = ROOT.TEfficiency(h_jetMult[tg], h_jetMult["notrigger"])
                # xTitle = h_jetMult["notrigger"].GetXaxis().GetTitle()
                xBinWidth = h_jetMult["notrigger"].GetXaxis().GetBinWidth(1)
                h_TriggerRatio[tg].SetTitle(";Number of Jets ;Trigger Efficiency per {0} GeV/c".format(xBinWidth))
                h_TriggerRatio[tg].SetName(tg)
                h_TriggerRatio[tg].SetTitle(tg)
                h_TriggerRatio[tg].SetLineColor(j)
                j += 1
                if i == 0:
                    h_TriggerRatio[tg].Draw('AP')
                    cv4.Update()
                    graph1 = h_TriggerRatio[tg].GetPaintedGraph()
                    graph1.SetMinimum(0)
                    graph1.SetMaximum(1.2)
                    cv4.Update()
                    tX1 = 0.05 * ((h_jetMult["notrigger"].GetXaxis().GetXmax())-5)+5
                    tY1 = 1.1
                if i > 0:
                    h_TriggerRatio[tg].Draw('same')
            i += 1
    cv4.BuildLegend(0.5, 0.1, 0.9, 0.3)
    ROOT.gStyle.SetLegendTextSize(0.02)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    pdfCreator(argms, 1, triggerCanvas)

    # - B tagged Jet Multiplicity plots ---------------------------
    cv5 = triggerCanvas.cd(1)
    # h_jetBMult["notrigger"].SetTitle("")
    h_jetBMult["notrigger"].GetXaxis().SetRange(1, 10)
    h_jetBMult["notrigger"].Draw('E1')
    for key in trigList:
        if not key.find("Mu") == -1: continue
        for tg in trigList[key]:
            h_jetBMult[tg].Draw('E1 same')
    cv5.BuildLegend(0.57, 0.54, 0.97, 0.74)
    ROOT.gStyle.SetLegendTextSize(0.02)
    tX1 = 0.6 * (h_jetBMult["notrigger"].GetXaxis().GetXmax())
    tY1 = 0.95 * (h_jetBMult["notrigger"].GetMaximum())
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    pdfCreator(argms, 1, triggerCanvas)

    cv6 = triggerCanvas.cd(1)
    i = 0
    j = 2
    for key in trigList:
        if not key.find("Mu") == -1: continue
        for tg in trigList[key]:
            if ROOT.TEfficiency.CheckConsistency(h_jetBMult[tg], h_jetBMult["notrigger"]):
                h_TriggerRatio[tg] = ROOT.TEfficiency(h_jetBMult[tg], h_jetBMult["notrigger"])
                xTitle = h_jetBMult["notrigger"].GetXaxis().GetTitle()
                xBinWidth = h_jetBMult["notrigger"].GetXaxis().GetBinWidth(1)
                h_TriggerRatio[tg].SetTitle(";{0};Trigger Efficiency per {1} GeV/c".format(xTitle, xBinWidth))
                h_TriggerRatio[tg].SetName(tg)
                h_TriggerRatio[tg].SetTitle(tg)
                h_TriggerRatio[tg].SetLineColor(j)
                j += 1
                if i == 0:
                    h_TriggerRatio[tg].Draw('AP')
                    cv6.Update()
                    graph1 = h_TriggerRatio[tg].GetPaintedGraph()
                    graph1.SetMinimum(0)
                    graph1.SetMaximum(1.2)
                    cv6.Update()
                    tX1 = 0.05 * (h_jetBMult["notrigger"].GetXaxis().GetXmax())
                    tY1 = 1.1
                if i > 0:
                    h_TriggerRatio[tg].Draw('same')
            i += 1
    cv6.BuildLegend(0.5, 0.1, 0.9, 0.3)
    ROOT.gStyle.SetLegendTextSize(0.02)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    pdfCreator(argms, 1, triggerCanvas)

    # # - Muon test Plots-------------------------------
    triggerCanvas.cd(1)
    h_elGenPartFlav.Draw()
    pdfCreator(argms, 1, triggerCanvas)

    triggerCanvas.cd(1)
    h_elGenPartIdx.Draw()
    pdfCreator(argms, 1, triggerCanvas)

    triggerCanvas.cd(1)
    h_elMiniPfRelIso_all.Draw()
    pdfCreator(argms, 1, triggerCanvas)

    # - Muon pT plots ---------------------------------
    cv7 = triggerCanvas.cd(1)
    # h_elPt["notrigger"].SetTitle("")
    h_elPt["notrigger"].SetMinimum(0.)
    # h_elPt["notrigger"].SetMaximum(3500)
    h_elPt["notrigger"].Draw('E1')
    tX1 = 0.60*(h_elPt["notrigger"].GetXaxis().GetXmax())
    tY1 = 0.95*(h_elPt["notrigger"].GetMaximum())
    for key in trigList:
        if not key.find("Mu") == -1: continue
        for tg in trigList[key]:
            h_elPt[tg].Draw('E1 same')
    cv7.BuildLegend(0.57, 0.54, 0.97, 0.74)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    ROOT.gStyle.SetLegendTextSize(0.02)
    pdfCreator(argms, 1, triggerCanvas)

    cv71 = triggerCanvas.cd(1)
    h_elPt["notrigger"].SetTitle("")
    h_elPt["notrigger"].SetMinimum(0.)
    h_elPt["notrigger"].SetMaximum(3500)
    h_elPt["notrigger"].Draw('E1')
    tX1 = 0.6*(h_elPt["notrigger"].GetXaxis().GetXmax())
    tY1 = 0.95*(h_elPt["notrigger"].GetMaximum())
    h_elPt["prompt"].SetTitle("prompt muons")
    h_elPt["prompt"].Draw('E1 same')
    h_elPt["non-prompt"].Draw('E1 same')
    cv71.BuildLegend(0.57, 0.54, 0.97, 0.74)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    ROOT.gStyle.SetLegendTextSize(0.02)
    pdfCreator(argms, 1, triggerCanvas)

    cv8 = triggerCanvas.cd(1)
    i = 0
    j = 2
    for key in trigList:
        if not key.find("Mu") == -1: continue
        for tg in trigList[key]:
            if ROOT.TEfficiency.CheckConsistency(h_elPt[tg], h_elPt["notrigger"]):
                h_TriggerRatio[tg] = ROOT.TEfficiency(h_elPt[tg], h_elPt["notrigger"])
                xTitle = h_elPt["notrigger"].GetXaxis().GetTitle()
                xBinWidth = h_elPt["notrigger"].GetXaxis().GetBinWidth(1)
                h_TriggerRatio[tg].SetTitle(";{0};Trigger Efficiency per {1} GeV/c".format(xTitle, xBinWidth))
                h_TriggerRatio[tg].SetName(tg)
                h_TriggerRatio[tg].SetTitle(tg)
                h_TriggerRatio[tg].SetLineColor(j)
                j += 1
                if i == 0:
                    h_TriggerRatio[tg].Draw('AP')
                    cv8.Update()
                    graph1 = h_TriggerRatio[tg].GetPaintedGraph()
                    graph1.SetMinimum(0)
                    graph1.SetMaximum(1.2)
                    cv8.Update()
                    tX1 = 0.05 * (h_elPt["notrigger"].GetXaxis().GetXmax())
                    tY1 = 1.1
                if i > 0:
                    h_TriggerRatio[tg].Draw('same')
            i += 1
    cv8.BuildLegend(0.5, 0.1, 0.9, 0.3)
    ROOT.gStyle.SetLegendTextSize(0.02)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    pdfCreator(argms, 1, triggerCanvas)

    # - MET pT plots ---------------------------------
    cv9 = triggerCanvas.cd(1)
    h_metPt["notrigger"].GetXaxis().SetTitle("E^{Miss}_{T}")
    h_metPt["notrigger"].SetMinimum(0.)
    # h_metPt["notrigger"].SetMaximum(1800)
    h_metPt["notrigger"].Draw('E1')
    tX1 = 0.6 * (h_metPt["notrigger"].GetXaxis().GetXmax())
    tY1 = 0.95 * (h_metPt["notrigger"].GetMaximum())
    for key in trigList:
        if not key.find("Mu") == -1: continue
        for tg in trigList[key]:
            h_metPt[tg].Draw('E1 same')
    cv9.BuildLegend(0.57, 0.54, 0.97, 0.74)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    ROOT.gStyle.SetLegendTextSize(0.02)
    pdfCreator(argms, 1, triggerCanvas)

    cv10 = triggerCanvas.cd(1)
    i = 0
    j = 2
    for key in trigList:
        if not key.find("Mu") == -1: continue
        for tg in trigList[key]:
            if ROOT.TEfficiency.CheckConsistency(h_metPt[tg], h_metPt["notrigger"]):
                h_TriggerRatio[tg] = ROOT.TEfficiency(h_metPt[tg], h_metPt["notrigger"])
                # xTitle = h_metPt["notrigger"].GetXaxis().GetTitle()
                xBinWidth = h_metPt["notrigger"].GetXaxis().GetBinWidth(1)
                h_TriggerRatio[tg].SetTitle(";E^{Miss}_{T};Trigger Efficiency per %.2f GeV/c" % xBinWidth)
                h_TriggerRatio[tg].SetName(tg)
                h_TriggerRatio[tg].SetTitle(tg)
                h_TriggerRatio[tg].SetLineColor(j)
                j += 1
                if i == 0:
                    h_TriggerRatio[tg].Draw('AP')
                    cv10.Update()
                    graph1 = h_TriggerRatio[tg].GetPaintedGraph()
                    graph1.SetMinimum(0)
                    graph1.SetMaximum(1.2)
                    cv10.Update()
                    tX1 = 0.05 * (h_metPt["notrigger"].GetXaxis().GetXmax())
                    tY1 = 1.1
                if i > 0:
                    h_TriggerRatio[tg].Draw('same')
            i += 1
    cv10.BuildLegend(0.5, 0.1, 0.9, 0.3)
    ROOT.gStyle.SetLegendTextSize(0.02)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    pdfCreator(argms, 1, triggerCanvas)

    # - GenMET pT plots ---------------------------------
    cv11 = triggerCanvas.cd(1)
    h_genMetPt["notrigger"].GetXaxis().SetTitle("Gen E^{Miss}_{T}")
    h_genMetPt["notrigger"].SetMinimum(0.)
    # h_genMetPt["notrigger"].SetMaximum(2000)
    h_genMetPt["notrigger"].Draw('E1')
    tX1 = 0.6 * (h_genMetPt["notrigger"].GetXaxis().GetXmax())
    tY1 = 0.95 * (h_genMetPt["notrigger"].GetMaximum())
    for key in trigList:
        if not key.find("Mu") == -1: continue
        for tg in trigList[key]:
            h_genMetPt[tg].Draw('E1 same')
    cv11.BuildLegend(0.57, 0.54, 0.97, 0.74)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    ROOT.gStyle.SetLegendTextSize(0.02)
    pdfCreator(argms, 1, triggerCanvas)

    cv12 = triggerCanvas.cd(1)
    i = 0
    j = 2
    for key in trigList:
        if not key.find("Mu") == -1: continue
        for tg in trigList[key]:
            if ROOT.TEfficiency.CheckConsistency(h_genMetPt[tg], h_genMetPt["notrigger"]):
                h_TriggerRatio[tg] = ROOT.TEfficiency(h_genMetPt[tg], h_genMetPt["notrigger"])
                # xTitle = h_genMetPt["notrigger"].GetXaxis().GetTitle()
                xBinWidth = h_genMetPt["notrigger"].GetXaxis().GetBinWidth(1)
                h_TriggerRatio[tg].SetTitle("; Gen E^{Miss}_{T};Trigger Efficiency per %.2f GeV/c" % xBinWidth)
                h_TriggerRatio[tg].SetName(tg)
                h_TriggerRatio[tg].SetTitle(tg)
                h_TriggerRatio[tg].SetLineColor(j)
                j += 1
                if i == 0:
                    h_TriggerRatio[tg].Draw('AP')
                    cv12.Update()
                    graph1 = h_TriggerRatio[tg].GetPaintedGraph()
                    graph1.SetMinimum(0)
                    graph1.SetMaximum(1.2)
                    cv12.Update()
                    tX1 = 0.05 * (h_genMetPt["notrigger"].GetXaxis().GetXmax())
                    tY1 = 1.1
                if i > 0:
                    h_TriggerRatio[tg].Draw('same')
            i += 1
    cv12.BuildLegend(0.5, 0.1, 0.9, 0.3)
    ROOT.gStyle.SetLegendTextSize(0.02)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    pdfCreator(argms, 1, triggerCanvas)

    # - Eta plots ------------------------------------------
    cv13 = triggerCanvas.cd(1)
    # h_jetEta["notrigger"].GetYaxis().SetTitleOffset(1.1)
    h_jetEta["notrigger"].Draw('E1')
    tX1 = 0.6*6
    tY1 = 0.95*(h_jetEta["notrigger"].GetMaximum())
    for key in trigList:
        if not key.find("Mu") == -1: continue
        for tg in trigList[key]:
            h_jetEta[tg].Draw('E1 same')
    cv13.BuildLegend(0.4, 0.25, 0.4, 0.25)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    ROOT.gStyle.SetLegendTextSize(0.02)
    # pdfCreator(argms, 1, triggerCanvas)

    cv14 = triggerCanvas.cd(1)
    # h_elEta["notrigger"].GetYaxis().SetTitleOffset(1.2)
    h_elEta["notrigger"].Draw('E1')
    tX1 = 0.6*6
    tY1 = 0.95*(h_elEta["notrigger"].GetMaximum())
    for key in trigList:
        if not key.find("Mu") == -1: continue
        for tg in trigList[key]:
            h_elEta[tg].Draw('E1 same')
    cv14.BuildLegend(0.4, 0.25, 0.4, 0.25)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    ROOT.gStyle.SetLegendTextSize(0.02)
    pdfCreator(argms, 1, triggerCanvas)

    cv15 = triggerCanvas.cd(1)
    i = 0
    j = 2
    for key in trigList:
        if not key.find("Mu") == -1: continue
        for tg in trigList[key]:
            if ROOT.TEfficiency.CheckConsistency(h_elEta[tg], h_elEta["notrigger"]):
                h_TriggerRatio[tg] = ROOT.TEfficiency(h_elEta[tg], h_elEta["notrigger"])
                xTitle = h_elEta["notrigger"].GetXaxis().GetTitle()
                xBinWidth = h_elEta["notrigger"].GetXaxis().GetBinWidth(1)
                h_TriggerRatio[tg].SetTitle(";{0};Trigger Efficiency per {1} GeV/c".format(xTitle, xBinWidth))
                h_TriggerRatio[tg].SetName(tg)
                h_TriggerRatio[tg].SetTitle(tg)
                h_TriggerRatio[tg].SetLineColor(j)
                j += 1
                if i == 0:
                    h_TriggerRatio[tg].Draw('AP')
                    cv15.Update()
                    graph1 = h_TriggerRatio[tg].GetPaintedGraph()
                    graph1.SetMinimum(0)
                    graph1.SetMaximum(1.2)
                    cv15.Update()
                    tX1 = 0.05 * (h_elEta["notrigger"].GetXaxis().GetXmax())
                    tY1 = 1.1
                if i > 0:
                    h_TriggerRatio[tg].Draw('same')
            i += 1
    cv15.BuildLegend(0.5, 0.1, 0.9, 0.3)
    ROOT.gStyle.SetLegendTextSize(0.02)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    pdfCreator(argms, 1, triggerCanvas)

    # - Phi plots ------------------------------------------
    cv16 = triggerCanvas.cd(1)
    # h_jetPhi["notrigger"].GetYaxis().SetTitleOffset(1.3)
    h_jetPhi["notrigger"].Draw('E1')
    tX1 = 0.6*6
    tY1 = 0.95*(h_jetPhi["notrigger"].GetMaximum())
    for key in trigList:
        if not key.find("Mu") == -1: continue
        for tg in trigList[key]:
            h_jetPhi[tg].Draw('E1 same')
    cv16.BuildLegend(0.4, 0.2, 0.4, 0.2)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    ROOT.gStyle.SetLegendTextSize(0.02)
    # pdfCreator(argms, 1, triggerCanvas)

    cv17 = triggerCanvas.cd(1)
    # h_elPhi["notrigger"].GetYaxis().SetTitleOffset(1.4)
    h_elPhi["notrigger"].Draw('E1')
    tX1 = 0.6*6
    tY1 = 0.97*(h_elPhi["notrigger"].GetMaximum())
    for key in trigList:
        if not key.find("Mu") == -1: continue
        for tg in trigList[key]:
            h_elPhi[tg].Draw('E1 same')
    cv17.BuildLegend(0.4, 0.2, 0.4, 0.2)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    ROOT.gStyle.SetLegendTextSize(0.02)
    # pdfCreator(argms, 1, triggerCanvas)

    # - Eta-Phi Map plots ------------------------------------------
    triggerCanvas.cd(1)
    h_jetMap["notrigger"].Draw('COLZ')  # CONT4Z
    # pdfCreator(argms, 1, triggerCanvas)
    for key in trigList:
        if not key.find("Mu") == -1: continue
        for tg in trigList[key]:
            h_jetMap[tg].Draw('COLZ')
            # pdfCreator(argms, 1, triggerCanvas)

    h_elMap["notrigger"].Draw('COLZ')
    # pdfCreator(argms, 1, triggerCanvas)
    for key in trigList:
        if not key.find("Mu") == -1: continue
        for tg in trigList[key]:
            h_elMap[tg].Draw('COLZ')  # E
            # pdfCreator(argms, 1, triggerCanvas)

    #############################################################################
    # - Test Event numbers along steps ----------
    triggerCanvas.cd(1)
    h_eventsPrg.SetFillColor(ROOT.kAzure-9)
    h_eventsPrg.GetXaxis().SetLabelOffset(999)
    h_eventsPrg.GetXaxis().SetLabelSize(0)
    h_eventsPrg.Draw()
    tY1 = 0.05*(h_eventsPrg.GetMaximum())
    ltx.SetTextAngle(88)
    ltx.DrawLatex(0.5, tY1, "Pre-selection")
    ltx.DrawLatex(1.5, tY1, "Post-selection")
    i = 0
    for key in trigList:
        if not key.find("Mu") == -1: continue
        for tg in trigList[key]:
            ltx.DrawLatex((9.5 - i), tY1, tg)
            i += 1

    # h.GetXAxis().SetBinLabel(binnumber,string)
    pdfCreator(argms, 2, triggerCanvas)

    histFile.Close()


main(process_arguments())
