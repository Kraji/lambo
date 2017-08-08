clear
close all
set(0,'DefaultFigureWindowStyle','docked')
%%


%trend=zeros(1,1000);
% for i=1:length(trend)/2
%     trend(2*i-1)=1;
%     trend(2*i)=0;
% end


trend=randi(3,1000,1)';
%trend=(1+(-1).^[0:999])/2;
%trend=1.^[0:999];

%kk=10;
%error=zeros(1,15);
kk=5;
ctw=ctwalgorithm(trend,3,kk);

%[maxi_p,index_p]=max(ctw);
%prediction=index_p-1;

%prediction(length(prediction)-5:length(prediction));
'début'
ctw(:,1:10)
'fin'
ctw(:,length(ctw)-5:length(ctw))

%error(kk)=sum(abs(trend(1,kk+1:length(trend))-prediction))/(length(trend)-kk);
