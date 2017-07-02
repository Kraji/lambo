function [Px_record, countTree, betaTree, x]= ctw_live_update(x,xt,Nx,D,Px_record,countTree,betaTree)

indexweight = Nx.^[0:D-1];
offset = (Nx^(D) - 1) / (Nx-1) + 1;

context = x(length(x)-D+1:length(x));
leafindex = context*indexweight'+offset;

eta = (countTree(1:Nx-1,leafindex)'+0.5)/(countTree(Nx,leafindex)+0.5);
% update the leaf

countTree(xt+1,leafindex) = countTree(xt+1,leafindex) + 1;
node =floor((leafindex+Nx-2)/Nx);

while ( node ~=0)
    [countTree, betaTree, eta] = ctwupdate(countTree,betaTree, eta, node, xt,1/2) ;
    node =floor((node+Nx-2)/Nx);
end

eta_sum = sum(eta)+1;
Px_record(:,length(Px_record)+1) = [eta 1]'/eta_sum ;

x= [x,xt];
