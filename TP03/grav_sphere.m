function g = grav_sphere(x, rho, r, p_x, p_z)
    G=6.674e-8;
    g = ((4./3)*pi*G*rho*p_z*r^3) ./ ( ((p_x - x).^2 + p_z.^2).^(3./2) );
end
