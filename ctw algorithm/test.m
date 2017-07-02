clear
close all
set(0,'DefaultFigureWindowStyle','docked')
%%


trend=zeros(1,1000);
for i=1:length(trend)/2
    trend(2*i-1)=1;
    trend(2*i)=0;
end

%kk=10;
error=zeros(1,15);
kk=2
ctw=ctwalgorithm(trend,2,kk);

[maxi_p,index_p]=max(ctw);
prediction=index_p-1;

prediction(-1)

%error(kk)=sum(abs(trend(1,kk+1:length(trend))-prediction))/(length(trend)-kk);
