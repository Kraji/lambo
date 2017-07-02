clear
close all
set(0,'DefaultFigureWindowStyle','docked')
%%

average_price=importdata('data_int_1_ETH_EUR.txt');

trend=zeros(1,length(average_price)-1);
for i=1:length(average_price)-1
    trend(i)=(average_price(i+1)-average_price(i)>0);    
end

%kk=10;
error=zeros(1,15);
for kk=1:15
ctw=ctwalgorithm(trend,2,kk);

[maxi_p,index_p]=max(ctw);
prediction=index_p-1;

error(kk)=sum(abs(trend(1,kk+1:length(trend))-prediction))/(length(trend)-kk);
end
plot(1:15,error)