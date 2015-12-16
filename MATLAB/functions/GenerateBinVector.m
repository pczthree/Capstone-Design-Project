function [ A ] = GenerateBinVector( N )
%GenerateBinVector Generates a random binary vector A of length N with
%values {-1, 1}
%   Theoretically a uniform distribution.

A = rand(1,N);
for i=1:N
   if A(i) > 0.5
       A(i) = 1;
   else
       A(i) = -1;
   end
end

end

