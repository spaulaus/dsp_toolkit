#pragma rtGlobals=1		// Use modern global access method.

Function ComputeEnergy(EventNum)
Variable EventNum

	Nvar SL = SL	//energy filter peaking time
	Nvar SG =SG	// energy filter gap time
	Nvar Tau	// decay time
	Nvar DeltaT	// time interval between samples
	Nvar NumPreSamples
	Nvar PulseNumber = PulseNumber	//which pulse in trace to apply filter to
	Nvar BL_sep = BL_sep
	
	Wave STJTrace = root:STJTrace		//detector waveform
	Wave TriggerPos = root:TriggerPos	// a wave containing the fast trigger positions in the waveform
										// usually only one (single pulse per trace)
	Wave xp=xp			// a wave containing the limits of the filter sum intervals 
	
	// Calculate energy filter coefficients
	Variable C0, Cg, C1, b1, off, x0, x1, x2, x3, x4, x5, energy, baseline, numbases, k, offnew, prevTrig
	
	b1=exp(-DeltaT/Tau)
	C0=-(1-b1)/(1-b1^SL)*b1^SL
	Cg=1-b1
	C1=(1-b1)/(1-b1^SL)
	
	// Calculate energy
	
	energy=C0*sum(STJTrace,xp[0],xp[1]) + Cg*sum(STJTrace,xp[2],xp[3]) + C1*sum(STJTrace,xp[4],xp[5])
	
	//calculate baselines on pre-trigger section of waveform.
	// need at least 2* SL + SG 
	off=TriggerPos[EventNum] -SL - 10
	prevTrig = 0
	
	numbases = floor( (off-prevTrig) / (SL+SG+SL))
	if(numbases == 0)
		printf "Warning: event # %d w/o baseline\r", EventNum
		baseline = 0
	else
		baseline = 0
		for(k=0; k<numbases; k+=1)
			offnew=off - (SL+SG+SL)*(k+1)
			x0=pnt2x(STJTrace, offnew)
			x1=pnt2x(STJTrace, offnew+SL-1)
			x2=pnt2x(STJTrace, offnew+SL)
			x3=pnt2x(STJTrace, offnew+SL+SG-1)
			x4=pnt2x(STJTrace, offnew+SL+SG)
			x5=pnt2x(STJTrace, offnew+2*SL+SG-1)
			baseline += C0*sum(STJTrace,x0,x1) + Cg*sum(STJTrace,x2,x3) + C1*sum(STJTrace,x4,x5)
		endfor
		baseline /= numbases					
	endif
	energy -= baseline
	return(energy)
End

Function Limits(EventNum, valid) 	// use filter parameters and trigger position to
Variable EventNum, valid		// calculate limits for filter sums,
	// set markes in trace duplicates to display limits in graph
	//valid ==0 ok
	//valid ==1 pileup
	//valid ==2 out of range

	Nvar SL
	Nvar SG
	Nvar Tau
	Nvar DeltaT
	Nvar FastLength 
	Nvar NumPreSamples 
	Nvar PulseNumber = PulseNumber	//which pulse in trace to apply filter to

	Wave STJTrace = root:STJTrace
	Wave TriggerPos = root:TriggerPos
	Wave sumlimits=root:sumlimits
	sumlimits=nan
	
	make/o/n=6 xp	//wave for filter posisions (std)
	
	// Calculate energy filter coefficients
	
	Variable C0, Cg, C1, b1, off, p0, p1, p2, p3, p4, p5,p6, p7
	Variable prevtrig, energy, baseline, numbases, k, offnew
		
		//Std
		p0=TriggerPos[EventNum] -SL - 10
		p1 = p0+SL-1
		p2 = p0+SL
		p3 = p0+SL+SG-1
		p4 = p0+SL+SG
		p5 = p0+2*SL+SG-1
		p7 = TriggerPos[EventNum] + SG +SL	// end of pileup inspection
		xp[0]=pnt2x(STJTrace, p0)		// beginning of  sum E0
		xp[1]=pnt2x(STJTrace, p1)		// end of sum E0
		xp[2]=pnt2x(STJTrace, p2)		// beginning of gap sum
		xp[3]=pnt2x(STJTrace, p3)		// end of gap sum
		xp[4]=pnt2x(STJTrace, p4)		// beginning of sum E1
		xp[5]=pnt2x(STJTrace, p5)		// end of sum E1
					
End