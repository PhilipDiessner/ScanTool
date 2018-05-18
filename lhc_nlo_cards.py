def paramcard_MRSSM(toformat):
    """
    toformat -- list of squark, gluino, scalar octet and pseudoscalar octet
    not checking octet mass constraint
    """
    return """###################################
## INFORMATION FOR LOOP
###################################
Block loop 
    1 1500 # MUR 

###################################
## INFORMATION FOR MASS
###################################
Block mass 
    6 1.720000e+02 # MT 
   15 1.777000e+00 # MTA 
   23 9.118760e+01 # MZ 
   25 1.250000e+02 # MH 
  1000001 {0[0]} # msdl 
  1000002 {0[1]} # msul 
  1000003 {0[2]} # mssl 
  1000004 {0[3]} # mscl 
  1000005 {0[4]} # msbl 
  1000006 {0[5]} # mstl 
  2000001 {0[6]} # msdr 
  2000002 {0[7]} # msur 
  2000003 {0[8]} # mssr 
  2000004 {0[9]} # mscr 
  2000005 {0[10]} # msbr 
  2000006 {0[11]} # mstr 
  3000021 {2} # mOs 
  3000022 {3} # mOp 
## Dependent parameters, given by model restrictions.
## Those values should be edited following the 
## analytical expression. MG5 ignores those values 
## but they are important for interfacing the output of MG5
## to external program such as Pythia.
  1 0.000000 # d : 0.0 
  2 0.000000 # u : 0.0 
  3 0.000000 # s : 0.0 
  4 0.000000 # c : 0.0 
  5 0.000000 # b : 0.0 
  11 0.000000 # e- : 0.0 
  12 0.000000 # ve : 0.0 
  13 0.000000 # mu- : 0.0 
  14 0.000000 # vm : 0.0 
  16 0.000000 # vt : 0.0 
  21 0.000000 # g : 0.0 
  22 0.000000 # a : 0.0 
  24 79.824360 # w+ : cmath.sqrt(MZ__exp__2/2. + cmath.sqrt(MZ__exp__4/4. - (aEW*cmath.pi*MZ__exp__2)/(Gf*sqrt__2))) 
  9000002 91.187600 # ghz : MZ 
  9000003 79.824360 # ghwp : MW 
  9000004 79.824360 # ghwm : MW 
  1000021 {1} # go : MD3 

###################################
## INFORMATION FOR MSOFT
###################################
Block msoft 
    1 {1} # MD3 

###################################
## INFORMATION FOR SMINPUTS
###################################
Block sminputs 
    1 1.279000e+02 # aEWM1 
    2 1.166370e-05 # Gf 
    3 1.184000e-01 # aS 

###################################
## INFORMATION FOR YUKAWA
###################################
Block yukawa 
    6 1.720000e+02 # ymt 
   15 1.777000e+00 # ymtau 

###################################
## INFORMATION FOR DECAY
###################################
DECAY   6 1.508336e+00 # WT 
DECAY  23 2.495200e+00 # WZ 
DECAY  24 2.085000e+00 # WW 
DECAY  25 4.070000e-03 # WH 
DECAY 1000021 0.000000e+01 # wdglu 
DECAY 3000021 0.000000e+01 # wOs 
DECAY 3000022 0.000000e+01 # wOp 
## Dependent parameters, given by model restrictions.
## Those values should be edited following the 
## analytical expression. MG5 ignores those values 
## but they are important for interfacing the output of MG5
## to external program such as Pythia.
DECAY  1 0.000000 # d : 0.0 
DECAY  2 0.000000 # u : 0.0 
DECAY  3 0.000000 # s : 0.0 
DECAY  4 0.000000 # c : 0.0 
DECAY  5 0.000000 # b : 0.0 
DECAY  11 0.000000 # e- : 0.0 
DECAY  12 0.000000 # ve : 0.0 
DECAY  13 0.000000 # mu- : 0.0 
DECAY  14 0.000000 # vm : 0.0 
DECAY  15 0.000000 # ta- : 0.0 
DECAY  16 0.000000 # vt : 0.0 
DECAY  21 0.000000 # g : 0.0 
DECAY  22 0.000000 # a : 0.0 
DECAY  1000001 0.000000 # dl : 0.0 
DECAY  1000002 0.000000 # ul : 0.0 
DECAY  1000003 0.000000 # sl : 0.0 
DECAY  1000004 0.000000 # cl : 0.0 
DECAY  1000005 0.000000 # b1 : 0.0 
DECAY  1000006 0.000000 # t1 : 0.0 
DECAY  2000001 0.000000 # dr : 0.0 
DECAY  2000002 0.000000 # ur : 0.0 
DECAY  2000003 0.000000 # sr : 0.0 
DECAY  2000004 0.000000 # cr : 0.0 
DECAY  2000005 0.000000 # b2 : 0.0 
DECAY  2000006 0.000000 # t2 : 0.0 
DECAY  9000002 2.495200 # ghz : WZ 
DECAY  9000003 2.085000 # ghwp : WW 
DECAY  9000004 2.085000 # ghwm : WW 
#===========================================================
# QUANTUM NUMBERS OF NEW STATE(S) (NON SM PDG CODE)
#===========================================================

Block QNUMBERS 3000021  # sig8s 
        1 0  # 3 times electric charge
        2 1  # number of spin states (2S+1)
        3 8  # colour rep (1: singlet, 3: triplet, 8: octet)
        4 0  # Particle/Antiparticle distinction (0=own anti)
Block QNUMBERS 3000022  # sig8p 
        1 0  # 3 times electric charge
        2 1  # number of spin states (2S+1)
        3 8  # colour rep (1: singlet, 3: triplet, 8: octet)
        4 0  # Particle/Antiparticle distinction (0=own anti)
Block QNUMBERS 1000021  # go 
        1 0  # 3 times electric charge
        2 2  # number of spin states (2S+1)
        3 8  # colour rep (1: singlet, 3: triplet, 8: octet)
        4 1  # Particle/Antiparticle distinction (0=own anti)
Block QNUMBERS 1000002  # ul 
        1 2  # 3 times electric charge
        2 1  # number of spin states (2S+1)
        3 3  # colour rep (1: singlet, 3: triplet, 8: octet)
        4 1  # Particle/Antiparticle distinction (0=own anti)
Block QNUMBERS 1000004  # cl 
        1 2  # 3 times electric charge
        2 1  # number of spin states (2S+1)
        3 3  # colour rep (1: singlet, 3: triplet, 8: octet)
        4 1  # Particle/Antiparticle distinction (0=own anti)
Block QNUMBERS 1000006  # t1 
        1 2  # 3 times electric charge
        2 1  # number of spin states (2S+1)
        3 3  # colour rep (1: singlet, 3: triplet, 8: octet)
        4 1  # Particle/Antiparticle distinction (0=own anti)
Block QNUMBERS 2000002  # ur 
        1 2  # 3 times electric charge
        2 1  # number of spin states (2S+1)
        3 3  # colour rep (1: singlet, 3: triplet, 8: octet)
        4 1  # Particle/Antiparticle distinction (0=own anti)
Block QNUMBERS 2000004  # cr 
        1 2  # 3 times electric charge
        2 1  # number of spin states (2S+1)
        3 3  # colour rep (1: singlet, 3: triplet, 8: octet)
        4 1  # Particle/Antiparticle distinction (0=own anti)
Block QNUMBERS 2000006  # t2 
        1 2  # 3 times electric charge
        2 1  # number of spin states (2S+1)
        3 3  # colour rep (1: singlet, 3: triplet, 8: octet)
        4 1  # Particle/Antiparticle distinction (0=own anti)
Block QNUMBERS 1000001  # dl 
        1 -1  # 3 times electric charge
        2 1  # number of spin states (2S+1)
        3 3  # colour rep (1: singlet, 3: triplet, 8: octet)
        4 1  # Particle/Antiparticle distinction (0=own anti)
Block QNUMBERS 1000003  # sl 
        1 -1  # 3 times electric charge
        2 1  # number of spin states (2S+1)
        3 3  # colour rep (1: singlet, 3: triplet, 8: octet)
        4 1  # Particle/Antiparticle distinction (0=own anti)
Block QNUMBERS 1000005  # b1 
        1 -1  # 3 times electric charge
        2 1  # number of spin states (2S+1)
        3 3  # colour rep (1: singlet, 3: triplet, 8: octet)
        4 1  # Particle/Antiparticle distinction (0=own anti)
Block QNUMBERS 2000001  # dr 
        1 -1  # 3 times electric charge
        2 1  # number of spin states (2S+1)
        3 3  # colour rep (1: singlet, 3: triplet, 8: octet)
        4 1  # Particle/Antiparticle distinction (0=own anti)
Block QNUMBERS 2000003  # sr 
        1 -1  # 3 times electric charge
        2 1  # number of spin states (2S+1)
        3 3  # colour rep (1: singlet, 3: triplet, 8: octet)
        4 1  # Particle/Antiparticle distinction (0=own anti)
Block QNUMBERS 2000005  # b2 
        1 -1  # 3 times electric charge
        2 1  # number of spin states (2S+1)
        3 3  # colour rep (1: singlet, 3: triplet, 8: octet)
        4 1  # Particle/Antiparticle distinction (0=own anti)
""".format(*toformat)

def paramcard_mrssm_wrapper(toformat):
    """check if same squark masses or not"""
    if type(toformat[0])== type('str'):
        toformat[0]=[toformat[0]]*12
    return paramcard_MRSSM(toformat)
        

def runcard(toformat):
    """toformat is a list of runtag, lhapdfnumber"""
    return """#***********************************************************************
# Tag name for the run (one word)                                      *
#***********************************************************************
  {0}     = run_tag ! name of the run 
#***********************************************************************
# Number of LHE events (and their normalization) and the required      *
# (relative) accuracy on the Xsec.                                     *
# These values are ignored for fixed order runs                        *
#***********************************************************************
 10000 = nevents ! Number of unweighted events requested 
 -1.0 = req_acc ! Required accuracy (-1=auto determined from nevents)
 -1 = nevt_job! Max number of events per job in event generation. 
                 !  (-1= no split).
#***********************************************************************
# Normalize the weights of LHE events such that they sum or average to *
# the total cross section                                              *
#***********************************************************************
 average = event_norm      ! average or sum
#***********************************************************************
# Number of points per itegration channel (ignored for aMC@NLO runs)   *
#***********************************************************************
 {2}   = req_acc_FO       ! Required accuracy (-1=ignored, and use the 
 	                   ! number of points and iter. below)
# These numbers are ignored except if req_acc_FO is equal to -1
 5000   = npoints_FO_grid  ! number of points to setup grids
 4      = niters_FO_grid   ! number of iter. to setup grids
 10000  = npoints_FO       ! number of points to compute Xsec
 6      = niters_FO        ! number of iter. to compute Xsec
#***********************************************************************
# Random number seed                                                   *
#***********************************************************************
 0    = iseed       ! rnd seed (0=assigned automatically=default))
#***********************************************************************
# Collider type and energy                                             *
#***********************************************************************
 1   = lpp1    ! beam 1 type (0 = no PDF)
 1   = lpp2    ! beam 2 type (0 = no PDF)
 6500.0   = ebeam1  ! beam 1 energy in GeV
 6500.0   = ebeam2  ! beam 2 energy in GeV
#***********************************************************************
:# PDF choice: this automatically fixes also alpha_s(MZ) and its evol.  *
#***********************************************************************
 lhapdf = pdlabel ! PDF set
 {1}  = lhaid   ! If pdlabel=lhapdf, this is the lhapdf number. Only 
              ! numbers for central PDF sets are allowed. Can be a list; 
              ! PDF sets beyond the first are included via reweighting.
#***********************************************************************
# Include the NLO Monte Carlo subtr. terms for the following parton    *
# shower (HERWIG6 | HERWIGPP | PYTHIA6Q | PYTHIA6PT | PYTHIA8)         *
# WARNING: PYTHIA6PT works only for processes without FSR!!!!          *
#***********************************************************************
  HERWIG6   = parton_shower
  1.0       = shower_scale_factor ! multiply default shower starting
                                  ! scale by this factor
#***********************************************************************
# Renormalization and factorization scales                             *
# (Default functional form for the non-fixed scales is the sum of      *
# the transverse masses divided by two of all final state particles    * 
# and partons. This can be changed in SubProcesses/set_scales.f or via *
# dynamical_scale_choice option)                                       *
#***********************************************************************
 {3}    = fixed_ren_scale  ! if .true. use fixed ren scale
 {3}    = fixed_fac_scale  ! if .true. use fixed fac scale
 {4}   = muR_ref_fixed    ! fixed ren reference scale 
 {4}   = muF_ref_fixed    ! fixed fact reference scale
 0 = dynamical_scale_choice ! Choose one (or more) of the predefined
           ! dynamical choices. Can be a list; scale choices beyond the
           ! first are included via reweighting
 1.0  = muR_over_ref  ! ratio of current muR over reference muR
 1.0  = muF_over_ref  ! ratio of current muF over reference muF
#*********************************************************************** 
# Reweight variables for scale dependence and PDF uncertainty          *
#***********************************************************************
 1.0, 2.0, 0.5 = rw_rscale ! muR factors to be included by reweighting
 1.0, 2.0, 0.5 = rw_fscale ! muF factors to be included by reweighting
 True = reweight_scale ! Reweight to get scale variation using the 
            ! rw_rscale and rw_fscale factors. Should be a list of 
            ! booleans of equal length to dynamical_scale_choice to
            ! specify for which choice to include scale dependence.
 True = reweight_PDF  ! Reweight to get PDF uncertainty. Should be a
            ! list booleans of equal length to lhaid to specify for
            !  which PDF set to include the uncertainties.
#***********************************************************************
# Store reweight information in the LHE file for off-line model-       *
# parameter reweighting at NLO+PS accuracy                             *
#***********************************************************************
 False = store_rwgt_info ! Store info for reweighting in LHE file
#***********************************************************************
# ickkw parameter:                                                     *
#   0: No merging                                                      *
#   3: FxFx Merging - WARNING! Applies merging only at the hard-event  *
#      level. After showering an MLM-type merging should be applied as *
#      well. See http://amcatnlo.cern.ch/FxFx_merging.htm for details. *
#   4: UNLOPS merging (with pythia8 only). No interface from within    *
#      MG5_aMC available, but available in Pythia8.                    *
#  -1: NNLL+NLO jet-veto computation. See arxiv:1412.8408 [hep-ph].    *
#***********************************************************************
 0        = ickkw
#***********************************************************************
#
#***********************************************************************
# BW cutoff (M+/-bwcutoff*Gamma). Determines which resonances are      *
# written in the LHE event file                                        *
#***********************************************************************
 15.0  = bwcutoff
#***********************************************************************
# Cuts on the jets. Jet clustering is performed by FastJet.            *
#  - When matching to a parton shower, these generation cuts should be *
#    considerably softer than the analysis cuts.                       *
#  - More specific cuts can be specified in SubProcesses/cuts.f        *
#***********************************************************************
  1.0  = jetalgo   ! FastJet jet algorithm (1=kT, 0=C/A, -1=anti-kT)
  0.7  = jetradius ! The radius parameter for the jet algorithm
 10.0  = ptj       ! Min jet transverse momentum
 -1.0  = etaj      ! Max jet abs(pseudo-rap) (a value .lt.0 means no cut)
#***********************************************************************
# Cuts on the charged leptons (e+, e-, mu+, mu-, tau+ and tau-)        *
# More specific cuts can be specified in SubProcesses/cuts.f           *
#***********************************************************************
  0.0  = ptl     ! Min lepton transverse momentum
 -1.0  = etal    ! Max lepton abs(pseudo-rap) (a value .lt.0 means no cut)
  0.0  = drll    ! Min distance between opposite sign lepton pairs
  0.0  = drll_sf ! Min distance between opp. sign same-flavor lepton pairs
  0.0  = mll     ! Min inv. mass of all opposite sign lepton pairs
 30.0  = mll_sf  ! Min inv. mass of all opp. sign same-flavor lepton pairs
#***********************************************************************
# Photon-isolation cuts, according to hep-ph/9801442. When ptgmin=0,   *
# all the other parameters are ignored.                                *
# More specific cuts can be specified in SubProcesses/cuts.f           *
#***********************************************************************
 20.0  = ptgmin    ! Min photon transverse momentum
 -1.0  = etagamma  ! Max photon abs(pseudo-rap)
  0.4  = R0gamma   ! Radius of isolation code
  1.0  = xn        ! n parameter of eq.(3.4) in hep-ph/9801442
  1.0  = epsgamma  ! epsilon_gamma parameter of eq.(3.4) in hep-ph/9801442
 True  = isoEM  ! isolate photons from EM energy (photons and leptons)
#***********************************************************************
# For aMCfast+APPLGRID use in PDF fitting (http://amcfast.hepforge.org)*
#***********************************************************************
 0 = iappl ! aMCfast switch (0=OFF, 1=prepare grids, 2=fill grids)
#***********************************************************************
""".format(*toformat)

def optioncard(toformat):
    return "launch\norder={}\nfixed_order=ON\n0\n0\n".format(toformat)

def paramcard_MSSM(toformat):
    return """######################################################################
## PARAM_CARD AUTOMATICALY GENERATED BY MG5 FOLLOWING UFO MODEL   ####
######################################################################
##                                                                  ##
##  Width set on Auto will be computed following the information    ##
##        present in the decay.py files of the model.               ##
##        See  arXiv:1402.1178 for more details.                    ##
##                                                                  ##
######################################################################

###################################
## INFORMATION FOR LOOP
###################################
Block loop 
    1 1000 # MU_R 

###################################
## INFORMATION FOR MASS
###################################
Block mass 
    6 1.720000e+02 # MT 
   15 1.777000e+00 # MTA 
   23 9.118760e+01 # MZ 
   25 1.250000e+02 # MH 
  1000001 {0} # MsdL 
  1000002 {0} # MsuL 
  1000003 {0} # MssL 
  1000004 {0} # MscL 
  1000005 {0} # MsbL 
  1000006 {0} # MstL 
  1000021 {1} # Mgo 
  1000022 1.000000e+01 # Mchi 
  2000001 {0} # MsdR 
  2000002 {0} # MsuR 
  2000003 {0} # MssR 
  2000004 {0} # MscR 
  2000005 {0} # MsbR 
  2000006 {2} # MstR 
## Dependent parameters, given by model restrictions.
## Those values should be edited following the 
## analytical expression. MG5 ignores those values 
## but they are important for interfacing the output of MG5
## to external program such as Pythia.
  1 0.000000 # d : 0.0 
  2 0.000000 # u : 0.0 
  3 0.000000 # s : 0.0 
  4 0.000000 # c : 0.0 
  5 0.000000 # b : 0.0 
  11 0.000000 # e- : 0.0 
  12 0.000000 # ve : 0.0 
  13 0.000000 # mu- : 0.0 
  14 0.000000 # vm : 0.0 
  16 0.000000 # vt : 0.0 
  21 0.000000 # g : 0.0 
  22 0.000000 # a : 0.0 
  24 79.824360 # w+ : cmath.sqrt(MZ__exp__2/2. + cmath.sqrt(MZ__exp__4/4. - (aEW*cmath.pi*MZ__exp__2)/(Gf*sqrt__2))) 
  9000002 91.187600 # ghz : MZ 
  9000003 79.824360 # ghwp : MW 
  9000004 79.824360 # ghwm : MW 

###################################
## INFORMATION FOR MSOFT
###################################
Block msoft 
    1 0.000000e+03 # MstLR 

###################################
## INFORMATION FOR SMINPUTS
###################################
Block sminputs 
    1 1.279000e+02 # aEWM1 
    2 1.166370e-05 # Gf 
    3 1.184000e-01 # aS 

###################################
## INFORMATION FOR YUKAWA
###################################
Block yukawa 
    6 1.720000e+02 # ymt 
   15 1.777000e+00 # ymtau 

###################################
## INFORMATION FOR DECAY
###################################
DECAY   6 1.508336e+00 # WT 
DECAY  23 2.495200e+00 # WZ 
DECAY  24 2.085000e+00 # WW 
DECAY  25 4.070000e-03 # WH 
DECAY 1000001 0.000000e+00 # WsdL 
DECAY 1000002 0.000000e+00 # WsuL 
DECAY 1000003 0.000000e+00 # WssL 
DECAY 1000004 0.000000e+00 # WscL 
DECAY 1000005 0.000000e+00 # WsbL 
DECAY 1000006 0.000000e+00 # WstL 
DECAY 1000021 0.000000e+01 # Wgo 
DECAY 2000001 0.000000e+00 # WsdR 
DECAY 2000002 0.000000e+00 # WsuR 
DECAY 2000003 0.000000e+00 # WssR 
DECAY 2000004 0.000000e+00 # WscR 
DECAY 2000005 0.000000e+00 # WsbR 
DECAY 2000006 0.000000e+00 # WstR 
## Dependent parameters, given by model restrictions.
## Those values should be edited following the 
## analytical expression. MG5 ignores those values 
## but they are important for interfacing the output of MG5
## to external program such as Pythia.
DECAY  1 0.000000 # d : 0.0 
DECAY  2 0.000000 # u : 0.0 
DECAY  3 0.000000 # s : 0.0 
DECAY  4 0.000000 # c : 0.0 
DECAY  5 0.000000 # b : 0.0 
DECAY  11 0.000000 # e- : 0.0 
DECAY  12 0.000000 # ve : 0.0 
DECAY  13 0.000000 # mu- : 0.0 
DECAY  14 0.000000 # vm : 0.0 
DECAY  15 0.000000 # ta- : 0.0 
DECAY  16 0.000000 # vt : 0.0 
DECAY  21 0.000000 # g : 0.0 
DECAY  22 0.000000 # a : 0.0 
DECAY  1000022 0.000000 # n1 : 0.0 
DECAY  9000002 2.495200 # ghz : WZ 
DECAY  9000003 2.085000 # ghwp : WW 
DECAY  9000004 2.085000 # ghwm : WW 
#===========================================================
# QUANTUM NUMBERS OF NEW STATE(S) (NON SM PDG CODE)
#===========================================================

Block QNUMBERS 1000021  # go 
        1 0  # 3 times electric charge
        2 2  # number of spin states (2S+1)
        3 8  # colour rep (1: singlet, 3: triplet, 8: octet)
        4 0  # Particle/Antiparticle distinction (0=own anti)
Block QNUMBERS 1000022  # n1 
        1 0  # 3 times electric charge
        2 2  # number of spin states (2S+1)
        3 1  # colour rep (1: singlet, 3: triplet, 8: octet)
        4 0  # Particle/Antiparticle distinction (0=own anti)
Block QNUMBERS 1000002  # ul 
        1 2  # 3 times electric charge
        2 1  # number of spin states (2S+1)
        3 3  # colour rep (1: singlet, 3: triplet, 8: octet)
        4 1  # Particle/Antiparticle distinction (0=own anti)
Block QNUMBERS 1000004  # cl 
        1 2  # 3 times electric charge
        2 1  # number of spin states (2S+1)
        3 3  # colour rep (1: singlet, 3: triplet, 8: octet)
        4 1  # Particle/Antiparticle distinction (0=own anti)
Block QNUMBERS 1000006  # t1 
        1 2  # 3 times electric charge
        2 1  # number of spin states (2S+1)
        3 3  # colour rep (1: singlet, 3: triplet, 8: octet)
        4 1  # Particle/Antiparticle distinction (0=own anti)
Block QNUMBERS 2000002  # ur 
        1 2  # 3 times electric charge
        2 1  # number of spin states (2S+1)
        3 3  # colour rep (1: singlet, 3: triplet, 8: octet)
        4 1  # Particle/Antiparticle distinction (0=own anti)
Block QNUMBERS 2000004  # cr 
        1 2  # 3 times electric charge
        2 1  # number of spin states (2S+1)
        3 3  # colour rep (1: singlet, 3: triplet, 8: octet)
        4 1  # Particle/Antiparticle distinction (0=own anti)
Block QNUMBERS 2000006  # t2 
        1 2  # 3 times electric charge
        2 1  # number of spin states (2S+1)
        3 3  # colour rep (1: singlet, 3: triplet, 8: octet)
        4 1  # Particle/Antiparticle distinction (0=own anti)
Block QNUMBERS 1000001  # dl 
        1 -1  # 3 times electric charge
        2 1  # number of spin states (2S+1)
        3 3  # colour rep (1: singlet, 3: triplet, 8: octet)
        4 1  # Particle/Antiparticle distinction (0=own anti)
Block QNUMBERS 1000003  # sl 
        1 -1  # 3 times electric charge
        2 1  # number of spin states (2S+1)
        3 3  # colour rep (1: singlet, 3: triplet, 8: octet)
        4 1  # Particle/Antiparticle distinction (0=own anti)
Block QNUMBERS 1000005  # b1 
        1 -1  # 3 times electric charge
        2 1  # number of spin states (2S+1)
        3 3  # colour rep (1: singlet, 3: triplet, 8: octet)
        4 1  # Particle/Antiparticle distinction (0=own anti)
Block QNUMBERS 2000001  # dr 
        1 -1  # 3 times electric charge
        2 1  # number of spin states (2S+1)
        3 3  # colour rep (1: singlet, 3: triplet, 8: octet)
        4 1  # Particle/Antiparticle distinction (0=own anti)
Block QNUMBERS 2000003  # sr 
        1 -1  # 3 times electric charge
        2 1  # number of spin states (2S+1)
        3 3  # colour rep (1: singlet, 3: triplet, 8: octet)
        4 1  # Particle/Antiparticle distinction (0=own anti)
Block QNUMBERS 2000005  # b2 
        1 -1  # 3 times electric charge
        2 1  # number of spin states (2S+1)
        3 3  # colour rep (1: singlet, 3: triplet, 8: octet)
        4 1  # Particle/Antiparticle distinction (0=own anti)
""".format(*toformat)
