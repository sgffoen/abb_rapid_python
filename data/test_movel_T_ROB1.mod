MODULE milling_basic_T_ROB1
VAR extjoint extj := [9E9,9E9,9E9,9E9,9E9,9E9];
VAR confdata conf := [0,0,0,0];
PERS tooldata Mill_Small:=[TRUE,[[302.106,-5.951,536.988],[0,0.38285,0,0.92381]],[6.75,[302.106,-5.951,536.988],[1,0,0,0],0,0,0]];
TASK PERS wobjdata DefaultFrame:=[FALSE,TRUE,"",[[0,0,0],[1,0,0,0]],[[0,0,0],[1,0,0,0]]];
TASK PERS speeddata Speed000:=[40,180,5000,1080];
TASK PERS speeddata Speed001:=[15,180,5000,1080];
TASK PERS zonedata Zone000:=[FALSE,3,3,3,0.3,3,0.3];
PROC Main()
ConfL \Off;
MoveAbsJ [[-5.7415,-3.6151,18.2351,7.9563,30.7462,-10.9146],extj],Speed000,Zone000,Mill_Small;
MoveJ [[1345.53,282.804,106.963],[0,1,0,0],[0,-2,0,0],extj],Speed000,Zone000,Mill_Small \WObj:=DefaultFrame;
WaitTime 0.3;
SetDO DO_2, 1;
SetDO VALVE_1, 1;
SetDO WAGO_Dust_Extraction, 1;
WaitTime 0.3;
SetAO AO_0, 400;
WaitTime 1.5;
MoveL [[1345.53,282.804,6.963],[0,1,0,0],conf,extj],Speed001,fine,Mill_Small \WObj:=DefaultFrame;
MoveL [[1342.334,-349.174,2.79],[0,1,0,0],conf,extj],Speed001,fine,Mill_Small \WObj:=DefaultFrame;
MoveL [[1342.334,-349.174,102.79],[0,1,0,0],conf,extj],Speed000,Zone000,Mill_Small \WObj:=DefaultFrame;
WaitTime 0.3;
SetDO DO_2, 0;
SetDO VALVE_1, 0;
SetDO WAGO_Dust_Extraction, 0;
WaitTime 0.3;
SetAO AO_0, 0;
WaitTime 0.3;
MoveAbsJ [[-5.7415,-3.6151,18.2351,7.9563,30.7462,-10.9146],extj],Speed000,Zone000,Mill_Small;
ENDPROC
ENDMODULE