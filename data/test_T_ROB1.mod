MODULE Positioner_T_ROB1
VAR confdata conf := [0,0,0,0];
PERS tooldata mill_test:=[TRUE,[[270.94,-4.707,504.723],[0,0.38285,0,0.92381]],[7,[270.94,-4.707,504.723],[1,0,0,0],0,0,0]];
TASK PERS wobjdata DefaultFrame:=[FALSE,TRUE,"",[[0,0,0],[1,0,0,0]],[[0,0,0],[1,0,0,0]]];
TASK PERS wobjdata Frame000:=[FALSE,FALSE,"STN1",[[1701.531,-720.42,649.1287],[1,0,0,0]],[[0,0,233],[0.707,0,0,0.707]]];
TASK PERS speeddata Speed000:=[70,180,5000,1080];
TASK PERS zonedata Zone000:=[FALSE,1,1,1,0.1,1,0.1];
PROC Main()
ConfL \Off;
ActUnit STN1;
MoveAbsJ [[0,-0,-0,0,45,0],[9E9,0,0,9E9,9E9,9E9]],Speed000,Zone000,mill_test;
MoveL [[1250,0,950],[0,1,0,0],conf,[9E9,0,0,9E9,9E9,9E9]],Speed000,fine,mill_test \WObj:=DefaultFrame;
Stop;
MoveJ [[0,-100,10],[-0.33088,0.62492,0.62492,0.33088],conf,[9E9,90,0,9E9,9E9,9E9]],Speed000,fine,mill_test \WObj:=Frame000;
MoveJ [[0,-75,10],[-0.33088,0.62492,0.62492,0.33088],conf,[9E9,90,0,9E9,9E9,9E9]],Speed000,fine,mill_test \WObj:=Frame000;
MoveJ [[0,-50,10],[-0.33088,0.62492,0.62492,0.33088],conf,[9E9,90,0,9E9,9E9,9E9]],Speed000,fine,mill_test \WObj:=Frame000;
MoveJ [[0,-25,10],[-0.33088,0.62492,0.62492,0.33088],conf,[9E9,90,0,9E9,9E9,9E9]],Speed000,fine,mill_test \WObj:=Frame000;
MoveJ [[0,25,10],[0.33088,0.62492,-0.62492,0.33088],conf,[9E9,90,-180,9E9,9E9,9E9]],Speed000,fine,mill_test \WObj:=Frame000;
MoveJ [[0,50,10],[0.33088,0.62492,-0.62492,0.33088],conf,[9E9,90,-180,9E9,9E9,9E9]],Speed000,fine,mill_test \WObj:=Frame000;
MoveJ [[0,75,10],[0.33088,0.62492,-0.62492,0.33088],conf,[9E9,90,-180,9E9,9E9,9E9]],Speed000,fine,mill_test \WObj:=Frame000;
MoveJ [[0,100,10],[0.33088,0.62492,-0.62492,0.33088],conf,[9E9,90,-180,9E9,9E9,9E9]],Speed000,fine,mill_test \WObj:=Frame000;
MoveJ [[0,-100,20],[-0.33088,0.62492,0.62492,0.33088],conf,[9E9,90,0,9E9,9E9,9E9]],Speed000,fine,mill_test \WObj:=Frame000;
MoveJ [[0,-75,20],[-0.33088,0.62492,0.62492,0.33088],conf,[9E9,90,0,9E9,9E9,9E9]],Speed000,fine,mill_test \WObj:=Frame000;
MoveJ [[0,-50,20],[-0.33088,0.62492,0.62492,0.33088],conf,[9E9,90,0,9E9,9E9,9E9]],Speed000,fine,mill_test \WObj:=Frame000;
MoveJ [[0,-25,20],[-0.33088,0.62492,0.62492,0.33088],conf,[9E9,90,0,9E9,9E9,9E9]],Speed000,fine,mill_test \WObj:=Frame000;
MoveJ [[0,25,20],[0.33088,0.62492,-0.62492,0.33088],conf,[9E9,90,-180,9E9,9E9,9E9]],Speed000,fine,mill_test \WObj:=Frame000;
MoveJ [[0,25,160],[0.33088,0.62492,-0.62492,0.33088],conf,[9E9,90,-180,9E9,9E9,9E9]],Speed000,fine,mill_test \WObj:=Frame000;
MoveJ [[0,50,160],[0.33088,0.62492,-0.62492,0.33088],conf,[9E9,90,-180,9E9,9E9,9E9]],Speed000,fine,mill_test \WObj:=Frame000;
MoveJ [[0,75,160],[0.33088,0.62492,-0.62492,0.33088],conf,[9E9,90,-180,9E9,9E9,9E9]],Speed000,fine,mill_test \WObj:=Frame000;
MoveJ [[0,100,160],[0.33088,0.62492,-0.62492,0.33088],conf,[9E9,90,-180,9E9,9E9,9E9]],Speed000,fine,mill_test \WObj:=Frame000;
MoveJ [[0,-100,170],[-0.33088,0.62492,0.62492,0.33088],conf,[9E9,90,0,9E9,9E9,9E9]],Speed000,fine,mill_test \WObj:=Frame000;
MoveJ [[0,-75,170],[-0.33088,0.62492,0.62492,0.33088],conf,[9E9,90,0,9E9,9E9,9E9]],Speed000,fine,mill_test \WObj:=Frame000;
MoveJ [[0,-25,300],[-0.33088,0.62492,0.62492,0.33088],conf,[9E9,90,0,9E9,9E9,9E9]],Speed000,fine,mill_test \WObj:=Frame000;
MoveJ [[0,25,300],[0.33088,0.62492,-0.62492,0.33088],conf,[9E9,90,-180,9E9,9E9,9E9]],Speed000,fine,mill_test \WObj:=Frame000;
MoveJ [[0,50,300],[0.33088,0.62492,-0.62492,0.33088],conf,[9E9,90,-180,9E9,9E9,9E9]],Speed000,fine,mill_test \WObj:=Frame000;
MoveJ [[0,75,300],[0.33088,0.62492,-0.62492,0.33088],conf,[9E9,90,-180,9E9,9E9,9E9]],Speed000,fine,mill_test \WObj:=Frame000;
MoveJ [[0,100,300],[0.33088,0.62492,-0.62492,0.33088],conf,[9E9,90,-180,9E9,9E9,9E9]],Speed000,fine,mill_test \WObj:=Frame000;
MoveAbsJ [[0,-0,-0,0,45,0],[9E9,0,0,9E9,9E9,9E9]],Speed000,Zone000,mill_test;
ENDPROC
ENDMODULE