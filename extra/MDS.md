# Multidimensional scaling(MDS)
## 1 MDS简介
MDS,多维尺度分析，又名Principal Coordinates Analysis(主坐标分析)

MDS的主要目的是：给一个距离矩阵D，计算出矩阵D的相对位置矩阵X，使得通过X反过来计算距离矩阵与原矩阵D的差距最小

$$
 \min_{x_1,\ldots,x_n} \sum_{i \to j}(||x_i-x_j||-d_{ij})^2
$$

一般位置矩阵选择二维或者三维矩阵，可以便于作图来表示此矩阵。

上述构建的位置矩阵用的是欧氏距离，也可以选用其他的距离

## 2 MDS过程

![avatar](https://public.lightpic.info/image/D3C4_59C928B50.jpg)

## 3 MDS实例

这里是 [参考matlab源代码](http://blog.csdn.net/songrotek/article/details/42235097),原作者是csdn的songrotek同学

    clc;  
    clear all;  
    close all;  
  
    %distance matrix for: London, Cardiff, Birmingham, Manchester, York, and  
    %Glasgow.  
    d=[0,411,213,219,296,397;...  
    411,0,204,203,120,152;...  
    213,204,0,73,136,245;...  
    219,203,73,0,90,191;...  
    296,120,136,90,0,109;...  
    397,152,245,191,109,0];  
  
    n=size(d,1);  
    t=zeros(n,n);  
    for i=1:n  
        for j=1:n  
            t(i,j)=-0.5*(d(i,j)^2 -1/n*d(i,:)*d(i,:)' -1/n*d(:,j)'*d(:,j) +1/n^2*sum(sum(d.^2)));  
        end  
    end  
    [V,D] = eig(t)  
    X=V(:,1:2)*D(1:2,1:2).^(1/2);  
    scatter(-X(:,2),X(:,1));  
    axis([-300,300,-300,300]);

> R中可以使用 *cmdscale* 命令来进行mds分析

