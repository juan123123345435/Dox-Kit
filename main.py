#!/usr/bin/env python3
import sys, os, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core import auth, ui, config, net
from core.session import Session
from core.modules import dns, whois, ipinfo, phone, portscan, httpinfo, sslcert, subdomains

def recon_all(target, sess):
    dns.run(target, sess)
    whois.run(target, sess)
    ipinfo.run(target, sess)
    httpinfo.run(target, sess)
    sslcert.run(target, sess)
    subdomains.run(target, sess)
    portscan.run(target, sess)

def config_menu():
    while True:
        ui.clear(); ui.banner()
        print(ui.c("  ===== CONFIGURACION =====\n", "mag"))
        print(f"  [1] Ver proxy actual   : {net.get_proxy() or '(ninguno)'}")
        print(f"  [2] Ver DNS actual     : {net.get_dns()}")
        print(f"  [3] Ver IP publica     : {net.public_ip()}")
        print("  [4] Ver interfaces de red")
        print("  [5] Configurar proxy")
        print("  [6] Configurar DNS")
        print("  [0] Volver")
        op = ui.ask("Opcion")
        if op == "1": pass
        elif op == "2": pass
        elif op == "3": pass
        elif op == "4":
            print(net.interfaces()); input(ui.c("  Enter...", "dim"))
        elif op == "5":
            net.set_proxy(ui.ask("Proxy (http://ip:puerto, vacio=quitar)"))
            ui.ok("Proxy actualizado.")
        elif op == "6":
            if net.set_dns(ui.ask("DNS (ej 1.1.1.1)")):
                ui.ok("DNS actualizado.")
        elif op == "0":
            break

def main():
    cfg = config.load()
    ui.clear(); ui.banner()
    user = auth.login()
    if not user:
        ui.err("Acceso denegado."); sys.exit(1)
    ui.ok(f"Bienvenido, {user}\n")

    while True:
        ui.show_menu()
        op = ui.ask("Opcion")
        if op == "0":
            ui.ok("Saliendo..."); break
        if op == "10":
            config_menu(); continue

        target = ui.ask("Objetivo (dominio / IP / numero)")
        if not target: continue

        base = target
        outdir = os.path.join(cfg["output_dir"],
                              f"{base}_{datetime.datetime.now():%Y%m%d_%H%M%S}")
        sess = Session(outdir)
        try:
            if   op == "1": dns.run(target, sess)
            elif op == "2": whois.run(target, sess)
            elif op == "3": ipinfo.run(target, sess)
            elif op == "4": phone.run(target, sess)
            elif op == "5": portscan.run(target, sess)
            elif op == "6": httpinfo.run(target, sess)
            elif op == "7": sslcert.run(target, sess)
            elif op == "8": subdomains.run(target, sess)
            elif op == "9": recon_all(target, sess)
            else: ui.warn("Opcion invalida"); continue
        except KeyboardInterrupt:
            ui.warn("Interrumpido")
        txt, js = sess.save(base)
        ui.ok(f"Informe guardado: {txt}")

if __name__ == "__main__":
    main()