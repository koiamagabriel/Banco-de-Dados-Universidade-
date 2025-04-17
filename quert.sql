SELECT dl.id_professor
FROM disciplinaslecionadas dl
JOIN curso_disciplina cd ON dl.id_disciplina = cd.id_disciplina
GROUP BY dl.id_professor
HAVING COUNT(DISTINCT cd.id_curso) > 1;
