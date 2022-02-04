#include "generators.h"

void GenHemisphere(float stepY, int countPoints, int r){
    std::ofstream file("figures/hemisphere.obj", std::ofstream::out | std::ofstream::trunc);
    if(!file.is_open()){
        std::cout << "Can't open file\n";
    }
    else{
        float stepDgr = (float)360/countPoints;
        float x, y, z;
        int count = 0;
        for(y = 0; y < 2; y=y+stepY){
            count++;
            float alpha = asin((double)y/r);
            float firstx = r * cos(alpha);
            for(float dgr = 0; dgr < 360; dgr=dgr+stepDgr){
                x = firstx*cos(M_PI/180 * dgr);
                z = firstx*sin(M_PI/180 * dgr);
                file << "v " << x << " " << y << " " << z << "\n";
            }
        }
        file << "v 0 2 0\n";
        for(int i = 0; i < count-1; i++){
            for(int j = 0; j < countPoints; j++){
                file << "f " << j + i*countPoints+1 << " " <<  j+(i+1)*countPoints+1 << " " << (j+1)%countPoints + (i+1)*countPoints +1<< " " << (j+1)%countPoints + i*countPoints+1 << "\n";
            }
        }
        file << "f";
        for(int i = 1; i <= countPoints; i++){
            file << " " << i;
        }
        file << "\n";
        for(int i = 0; i < countPoints; i++){
            file << "f " << countPoints*(count-1) + i +1<< " " <<  countPoints*count << " " << countPoints*(count-1) + (i+1)%countPoints+1 << "\n";
        }
    }
    file.close();
}

void GenHourseshoe(int ring, int points, int R, int r){
    std::ofstream file("figures/horseshoe.obj", std::ofstream::out | std::ofstream::trunc);
    if(!file.is_open()){
        std::cout << "Can't open file\n";
    }
    else{
        float stepI = (float)200/ring;
        float stepJ = (float)360/points;
        float x, y, z;
        for(float i = 290, countR = 0; i > 90, countR < ring; i=i-stepI, countR++){
            for(float j = 0, countP = 0; j < 360.0f, countP < points; j=j+stepJ, countP++){
                x = (R+r*cos(M_PI/180 * j)) * sin(M_PI/180 * i);
                y = (R+r*cos(M_PI/180 * j)) * cos(M_PI/180 * i);
                z = r * sin(M_PI/180 * j);
                file << "v " << x << " " << y << " " << z << "\n";
            }
        }
        for(int i = 0; i < ring-1; i++){
            for(int j = 0; j < points; j++){
                file << "f " << j+i*points+1 << " " << j+(i+1)*points+1<< " " << (j+1)%points + (i+1)*points+1 << " " << (j+1)%points + i*points+1 << "\n";
            }
        }
        file << "f";
        for(int i = 1; i < points+1; i++){
            file << " " << i;
        }
        file << "\nf";
        for(int i = points; i > 0; i--){
            file << " " << i+(ring-1)*points;
        }
        file << "\n";
    }
    file.close();
}