questions = {
    'q_lavori_nel_calcio': {  # Unique ID for the question
        'question_text': 'Lavori nel calcio?',
        'category': 'Calcio',
        'answers': {
            'a_si': {  # Unique ID for the answer 'sì'
                'text': 'Sì',
                'points': 2,
                'sub_questions': {
                    'sq_che_ruolo_ricopri': {  # Unique ID for sub-question
                        'question_text': 'Che ruolo ricopri?',
                        'category': 'Calcio',
                        'answers': {
                            'a_prima_squadra': {  # Unique ID for each sub-answer
                                'text': 'Allenatore / collaboratore / dirigente in prima squadra',
                                'points': 3
                            },
                            'a_settore_giovanile': {
                                'text': 'Allenatore / collaboratore / dirigente nel settore giovanile',
                                'points': 1
                            },
                            'a_stage_universita': {
                                'text': 'Stage con università o corsi privati',
                                'points': 2
                            }
                        }
                    },
                    'sq_iscrizione_corso': {  # Another sub-question under 'sì'
                        'question_text': 'Stai valutando l’iscrizione al corso perché?',
                        'category': 'Personale',
                        'answers': {
                            'a_specializzarmi': {
                                'text': 'Voglio specializzarmi',
                                'points': 3
                            },
                            'a_certificarmi': {
                                'text': 'Voglio certificarmi',
                                'points': 2
                            },
                            'a_info_match_analyst': {
                                'text': 'Voglio informazioni su come lavora il match analyst',
                                'points': 1
                            }
                        }
                    }
                }
            },
            'a_no': {  # Unique ID for the answer 'no'
                'text': 'No',
                'points': 1,
                'sub_questions': {
                    'sq_calcio_come_lo_vedi': {
                        'question_text': 'Il calcio come lo vedi?',
                        'category': 'Calcio',
                        'answers': {
                            'a_tifoso_lavorare': {
                                'text': 'Sono un tifoso e voglio lavorare nel calcio',
                                'points': 1
                            },
                            'a_portare_conoscenze': {
                                'text': 'Come lavoratore vorrei portare le mie conoscenze e abilità nel calcio',
                                'points': 2
                            },
                            'a_matto_calcio': {
                                'text': 'Sono “matto calcio”, è la mia più grande passione',
                                'points': 3
                            }
                        }
                    },
                    'sq_iscrizione_corso': {  # Another sub-question under 'no'
                        'question_text': 'Stai valutando l’iscrizione al corso perché?',
                        'category': 'Personale',
                        'answers': {
                            'a_specializzarmi': {
                                'text': 'Voglio specializzarmi',
                                'points': 3
                            },
                            'a_certificarmi': {
                                'text': 'Voglio certificarmi',
                                'points': 2
                            },
                            'a_info_match_analyst': {
                                'text': 'Voglio informazioni su chi è il match analyst e che lavoro fa',
                                'points': 1
                            }
                        }
                    }
                }
            }
        }
    },
    'q_pc_windows_mac': {
        'question_text': 'Hai un PC Windows o un MAC?',
        'category': 'Tecnologia',
        'answers': {
            'a_windows': {
                'text': 'Windows',
                'points': 2,
            },
            'a_mac': {
                'text': 'Mac',
                'points': 2,
            },
            'a_no': {
                'text': 'Non ho un pc',
                'points': 2,
                'message': "Per poter iniziare a lavorare nel calcio come match analyst lo si può fare anche senza tecnologia. Carta e penna funzionano sempre."
            }
        }
    },
 
    'q_telefono': {
        'question_text': 'Che tipo di telefono hai?',
        'category': 'Tecnologia',
        'answers': {
            'a_android': {
                'text': 'Ho un cellulare android',
                'points': 2
            },
            'a_iphone': {
                'text': 'Ho un cellulare iphone',
                'points': 2
            },
            'a_android_tablet': {
                'text': 'Ho un cellulare android e pure un tablet o un ipad',
                'points': 3
            },
            'a_iphone_tablet': {
                'text': 'Ho un cellulare iphone e pure un tablet o un ipad',
                'points': 3
            }
        }
    },
    
    'q_importo_match_analyst': {
        'question_text': 'Qual è il miglior importo che vuoi pagare per diventare match analyst?',
        'category': 'Economico',
        'answers': {
            'a_10_euro': {
                'text': '10 euro',
                'points': 1
            },
            'a_47_euro': {
                'text': '47 euro',
                'points': 2
            },
            'a_97_euro': {
                'text': '97 euro',
                'points': 3
            },
            'a_gratis': {
                'text': 'Non voglio spendere soldi, voglio tutto gratis!!!',
                'points': -10
            }
        }
    }
}

score_ranges = {
    'START': {
        'range': (-200, 6),
        'message': "Ci rivediamo dopo il tuo compleanno. Festeggiare insieme a chi ti vuole bene sarà per te un momento importante per coinvolgere amici e parenti nell’aiutarti a raccogliere le risorse per iniziare a diventare match analyst. Ti aspettiamo."
    },
    'BEGINNER': {
        'range': (7, 10),
        'message': "**Benissimo!!! Uno, due, tre: partiamo. Benvenuto nel mondo dei match analyst.** Ti condivideremo la nostra migliore proposta di formazione che fa al caso tuo."
    },
    'CHAMPION': {
        'range': (11, 15),
        'message': "**Ci vuole passione e disciplina per entrare nel mondo del calcio e tu le hai. Siamo felici di insegnarti la nostra metodologia sulla match analysis.** Ti condivideremo la nostra migliore proposta di formazione che fa al caso tuo."
    },
    'GOLD': {
        'range': (16, 100),
        'message': "**Complimenti, il tuo profilo è veramente interessante. Saremo molto felici di aiutarti a raggiungere il tuo obbiettivo nel mondo del calcio.** Ti condivideremo la nostra migliore proposta di formazione che fa al caso tuo."
    }
}


