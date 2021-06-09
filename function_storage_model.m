function [P_el,SoC] = function_storage_model(P_Res,Cap)
c_rate_max = 0.95 ; % Max C-Rate [1/h]
efficiency_DCH = 0.98;  % Discharge efficiency
efficiency_CH = 0.98;  % Charge efficiency
boundary_DCH = 0.10;  % Discharge boundary
boundary_CH = 0.90;  % Charge boundary

capacity = Cap;
Residual_load = [0;P_Res];
SoC(1)=0.5;
battery_power_max = (c_rate_max*capacity);


for i=2:1:length(Residual_load)
 if  (  Residual_load(i) <0)
    %Charging Mode:
    P_el(i) = abs(Residual_load(i));
    if (P_el(i) > battery_power_max)
        P_el(i) = battery_power_max;
    else
        P_el(i) = P_el(i);
    end
    SoC(i) = SoC(i-1) + (P_el(i)*efficiency_CH/capacity);
    
    % Capacity Boundary:  SoC_new > SoC_max 
    if ( SoC(i) > boundary_CH )
        P_el(i) = (boundary_CH - SoC(i-1))*capacity/efficiency_CH;
        SoC(i) = boundary_CH;
    else
        P_el(i) = P_el(i);
    end
        
elseif (Residual_load(i) > 0)
    % Discharging mode
    P_el(i) = - Residual_load(i);
    if (abs(P_el(i)) >  battery_power_max)
        P_el(i) = -battery_power_max;
    else
        P_el(i) = P_el(i);
    end
    
    SoC(i) = SoC(i-1) + (P_el(i)/efficiency_DCH)/capacity;
    if (SoC(i) < boundary_DCH)
        P_el(i) = (boundary_DCH - SoC(i-1))*capacity*efficiency_DCH;
        SoC(i) = boundary_DCH;
    else
        P_el(i) = P_el(i);
    end
   
 else
     P_el(i)=0;
     SoC(i)=SoC(i-1);
 end
 
end

P_el=P_el(2:length(P_el));
end 


 