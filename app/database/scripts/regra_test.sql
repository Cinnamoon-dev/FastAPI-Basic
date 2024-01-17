---
-- Cargos
---

INSERT INTO cargo (id, nome) VALUES (1, 'admin');
ALTER SEQUENCE cargo_id_seq RESTART WITH 2;

---
-- User
---

INSERT INTO public.user (id, name, password, isverified, email, cargo_id) VALUES (1, 'pedro', '$6$rounds=656000$XKEEd0hGhLt6g0Vk$Or8a6DgbayHxpwQ.H9lsOlFLPGiLg2gprob1NqeS0Xu0TJytOFXJ5TTVv1xA/pSSK0kwECxACxaMSxOl781fU.', True, 'teste@email.com', 1);
ALTER SEQUENCE user_id_seq RESTART WITH 2;

---
-- Controllers
---

insert into controller (id, nome) values (1, 'usuario');
ALTER SEQUENCE controller_id_seq RESTART WITH 2;

---
--  Regras
---

---
--  Admin
---

INSERT INTO regra(id, action, cargo_id, controller_id, permitir) VALUES (1, 'all',   1, 1, True ); -- /usuario/all
INSERT INTO regra(id, action, cargo_id, controller_id, permitir) VALUES (2, 'view',  1, 1, True ); -- /usuario/view
INSERT INTO regra(id, action, cargo_id, controller_id, permitir) VALUES (3, 'add',   1, 1, False); -- /usuario/add
INSERT INTO regra(id, action, cargo_id, controller_id, permitir) VALUES (4, 'edit',  1, 1, True ); -- /usuario/edit
INSERT INTO regra(id, action, cargo_id, controller_id, permitir) VALUES (5, 'delete',1, 1, True ); -- /usuario/delete